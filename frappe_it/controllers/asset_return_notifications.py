# Copyright (c) 2025, buff0k and contributors
# For license information, please see license.txt

import frappe

IT_ROLES = ("IT Manager",)
IGNORE_FIELDS = {
    "name", "owner", "creation", "modified", "modified_by", "idx",
    "docstatus", "parent", "parenttype", "parentfield", "amended_from", "version"
}

def on_create(doc, method=None):
    _notify_it(doc=doc, action="created")

def on_update(doc, method=None):
    # Only notify if this is not the first insert and something actually changed
    before = doc.get_doc_before_save()
    if not before:
        return  # The 'created' handler will have handled first insert

    changed = _diff_changed_fields(doc, before)
    if changed:
        _notify_it(doc=doc, action="updated", changed_fields=changed)

def on_submit(doc, method=None):
    _notify_it(doc=doc, action="completed")

# ---------- helpers ----------

def _diff_changed_fields(curr_doc, prev_doc):
    changed = []
    curr = curr_doc.as_dict()
    prev = prev_doc.as_dict()
    for k, v in curr.items():
        if k in IGNORE_FIELDS:
            continue
        if prev.get(k) != v:
            changed.append(k)
    return changed

def _collect_recipients(doc):
    """Return (recipient_emails, user_display_by_email).
    Includes all users with IT Manager role + the document creator (owner).
    De-duplicates and filters to enabled users with email.
    """
    users = set()

    # 1) Users with target roles
    for role in IT_ROLES:
        rows = frappe.get_all(
            "Has Role",
            filters={"role": role, "parenttype": "User"},
            fields=["parent"],  # parent is User.name
        )
        users.update(r["parent"] for r in rows)

    # 2) Add the document creator (owner)
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

def _notify_it(doc, action, changed_fields=None):
    recipient_emails, name_by_email = _collect_recipients(doc)
    if not recipient_emails:
        return

    subject = f"An Asset Return for {doc.get('employee_name')} ({doc.get('employee')}) {action}"
    url = frappe.utils.get_url(doc.get_url())

    # Send a personalized email to each recipient (so "Dear {user}" works)
    for email in recipient_emails:
        full_name = name_by_email.get(email) or "IT Team"

        # Body exactly as requested, with personalized greeting
        lines = [
            f"Dear {full_name}",
            "",
            f"An Asset Return for {doc.get('employee_name')} ({doc.get('employee')}) at {doc.get('branch')} has been {action}",
            "",
            f"Click here {url} to view",
        ]

        # Optional: include a short “what changed” on updates
        if action == "updated" and changed_fields:
            lines.insert(3, "")  # spacing
            lines.insert(4, "Fields changed:")
            for f in changed_fields:
                lines.append(f"• {f}")

        message = "<br>".join(lines)

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message,
            # queue='short', delayed=True,  # enable if you prefer queued emails
        )
