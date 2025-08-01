import os, sys, traceback, logging
import frappe
import frappe.permissions as perms

_patched = False
_logger = None

def _get_file_logger():
    """Create a per-site file logger that always writes to sites/<site>/logs/perm_reset.log."""
    global _logger
    if _logger:
        return _logger

    # Ensure site context exists
    site = frappe.local.site
    if not site:
        # Shouldn't happen during migrate, but fail safe to stderr
        sys.stderr.write("patch_perm_logging: no site in context\n")
        sys.stderr.flush()

    log_path = frappe.get_site_path("logs", "perm_reset.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger("perm_reset_hard")
    logger.propagate = False  # don't go to root handlers / console if not wanted
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers on repeated imports
    if not logger.handlers:
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(fh)

    _logger = logger
    return _logger

def _log(msg):
    # Write to file and stderr to be 100% visible
    logger = _get_file_logger()
    logger.warning(msg)
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()

def patch_perm_logging():
    global _patched
    if _patched:
        return
    _patched = True

    _log(">>> patch_perm_logging() installed")

    # 1) Intercept explicit resets
    _orig_reset_perms = perms.reset_perms
    def _logged_reset_perms(dt, *a, **k):
        if dt == "Employee":
            _log("reset_perms(Employee) called:\n" + "".join(traceback.format_stack(limit=30)))
        return _orig_reset_perms(dt, *a, **k)
    perms.reset_perms = _logged_reset_perms

    # 2) Intercept frappe.db.delete on Custom DocPerm (covers ORM deletes)
    _orig_db_delete = frappe.db.delete
    def _logged_db_delete(doctype, filters=None, *a, **k):
        if doctype == "Custom DocPerm":
            try:
                parent = (filters or {}).get("parent")
            except Exception:
                parent = None
            if parent in ("Employee", None):
                _log(f"frappe.db.delete(Custom DocPerm, filters={filters})\n" +
                     "".join(traceback.format_stack(limit=30)))
        return _orig_db_delete(doctype, filters, *a, **k)
    frappe.db.delete = _logged_db_delete

    # 3) Intercept ANY raw SQL that deletes from tabCustom DocPerm (covers direct SQL)
    _orig_sql = frappe.db.sql
    def _logged_sql(query, *a, **k):
        try:
            q = query.decode() if isinstance(query, (bytes, bytearray)) else str(query)
        except Exception:
            q = str(query)
        low = q.lower()
        if "delete" in low and "tabcustom docperm" in low:
            _log("frappe.db.sql DELETE detected:\n" + q + "\n" +
                 "".join(traceback.format_stack(limit=30)))
        return _orig_sql(query, *a, **k)
    frappe.db.sql = _logged_sql
