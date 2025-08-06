# Copyright (c) 2025, buff0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.meta import get_meta

IT_ROLES = ("IT Manager",)
IGNORE_FIELDS = {
    "name", "owner", "creation", "modified", "modified_by", "idx",
    "docstatus", "parent", "parenttype", "parentfield", "amended_from", "version"
}


def handle_doc_event(doc, method, action, changed_fields=None):
    if doc.doctype == "Asset Request":
        return handle_notification(
            doc, action,
            subject_template="Asset Request for {employee_asset_name} ({allocate_to}) {action}",
            body_template="An Asset Request for {employee_asset_name} ({allocate_to}) at {allocate_to_site} has been {action} by {actor}.",
            changed_fields=changed_fields
        )
    elif doc.doctype == "Asset Return":
        return handle_notification(
            doc, action,
            subject_template="Asset Return for {employee_name} ({employee}) {action}",
            body_template="An Asset Return for {employee_name} ({employee}) at {branch} has been {action} by {actor}.",
            changed_fields=changed_fields
        )


def handle_doc_event_create(doc, method):
    return handle_doc_event(doc, method, "created")


def handle_doc_event_update(doc, method):
    before = doc.get_doc_before_save()
    if not before:
        return
    changed_fields = _diff_changed_fields(doc, before)
    if changed_fields:
        return handle_doc_event(doc, method, "updated", changed_fields)


def handle_doc_event_submit(doc, method):
    return handle_doc_event(doc, method, "submitted")


# ---------- helpers ----------

def handle_notification(doc, action, subject_template, body_template, changed_fields=None):
    recipient_emails, name_by_email = _collect_recipients(doc)
    if not recipient_emails:
        return

    subject = subject_template.format(**doc.as_dict(), action=action)
    url = frappe.utils.get_url(doc.get_url())

    actor = frappe.session.user
    actor_fullname = frappe.db.get_value("User", actor, "full_name") or actor

    for email in recipient_emails:
        full_name = name_by_email.get(email) or "IT Team"
        lines = [
            f"Dear {full_name}",
            "",
            body_template.format(**doc.as_dict(), action=action, actor=actor_fullname),
            ""
        ]

        if action == "updated" and changed_fields:
            meta = frappe.get_meta(doc.doctype)
            lines.append("Fields changed:")
            for fieldname, (old, new) in changed_fields.items():
                label = meta.get_label(fieldname) or fieldname
                if isinstance(new, list):
                    lines.append(f"• {label}:")
                    for line in new:
                        lines.append(f"&nbsp;&nbsp;– {line}")
                else:
                    lines.append(f"• {label}: {old} → {new}")
            lines.append("")

        lines.append(f'<a href="{url}">Click here to view</a>')

        message = "<br>".join(lines)

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message,
        )


def _collect_recipients(doc):
    users = set()

    for role in IT_ROLES:
        rows = frappe.get_all(
            "Has Role",
            filters={"role": role, "parenttype": "User"},
            fields=["parent"]
        )
        users.update(r["parent"] for r in rows)

    if doc.owner:
        users.add(doc.owner)

    recipient_emails = set()
    name_by_email = {}

    for user in users:
        enabled, email, full_name = frappe.db.get_value(
            "User", user, ["enabled", "email", "full_name"]
        ) or (0, None, None)
        if enabled and email:
            recipient_emails.add(email)
            name_by_email[email] = full_name or user

    return sorted(recipient_emails), name_by_email


def _diff_changed_fields(curr_doc, prev_doc):
    changed = {}
    curr = curr_doc.as_dict()
    prev = prev_doc.as_dict()
    meta = frappe.get_meta(curr_doc.doctype)

    for field in meta.fields:
        fieldname = field.fieldname
        fieldtype = field.fieldtype

        if fieldname in IGNORE_FIELDS:
            continue

        curr_value = curr.get(fieldname)
        prev_value = prev.get(fieldname)

        if fieldtype == "Table":
            diffs = _diff_child_table_rows(curr_value, prev_value)
            if diffs:
                changed[fieldname] = (None, diffs)
        else:
            if isinstance(curr_value, (int, float)) and isinstance(prev_value, (int, float)):
                if abs(curr_value - prev_value) > 1e-6:
                    changed[fieldname] = (prev_value, curr_value)
            elif str(curr_value) != str(prev_value):
                changed[fieldname] = (prev_value, curr_value)

    return changed


def _diff_child_table_rows(curr_rows, prev_rows):
    changes = []

    if not curr_rows and not prev_rows:
        return []

    curr_map = {row.get("name"): row for row in curr_rows or []}
    prev_map = {row.get("name"): row for row in prev_rows or []}

    for name, curr_row in curr_map.items():
        if name in prev_map:
            prev_row = prev_map[name]
            diffs = []
            for key in curr_row:
                if key in IGNORE_FIELDS or key in ("parent", "parenttype", "parentfield"):
                    continue
                if str(curr_row.get(key)) != str(prev_row.get(key)):
                    diffs.append(f"{key}: {prev_row.get(key)} → {curr_row.get(key)}")
            if diffs:
                changes.append(f"Row {curr_row.get('idx')}: " + ", ".join(diffs))
        else:
            changes.append(f"Row {curr_row.get('idx')}: added")

    for name in prev_map:
        if name not in curr_map:
            prev_idx = prev_map[name].get("idx", "?")
            changes.append(f"Row {prev_idx}: removed")

    return changes
