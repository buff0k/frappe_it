app_name = "frappe_it"
app_title = "Frappe IT"
app_publisher = "buff0k"
app_description = "IT Management using Frappe and ERPNext"
app_email = "buff0k@gmail.com"
app_license = "mit"
required_apps = ["frappe/erpnext", "frappe/hrms"]
fixtures = [
	{"dt": "Role", "filters": [["name", "in", [
		"IT Manager",
		"IT User"
	]]]},
	{"dt": "Custom DocPerm", "filters": [["role", "in", [
		"IT Manager",
		"IT User"
	]]]},
	{"dt": "Asset Category", "filters": [["name", "in", [
		"Cellphone Simcards",
		"Handheld Radio",
		"IP Cameras",
		"NVRs",
		"Vehicle Mounted Radio",
		"Cellular Telephone",
		"Laptop Computer"
	]]]},
	{"dt": "Item Group", "filters": [["name", "in", [
		"Cellphone Simcards",
		"Handheld Radio",
		"IP Cameras",
		"NVRs",
		"Vehicle Mounted Radio",
		"Cellular Telephone",
		"Laptop Computer"
	]]]}
]
after_migrate = [
	"frappe_it.setup.add_employee_doclinks.ensure_employee_links",
	"frappe_it.setup.add_asset_doclinks.ensure_asset_links"
]
doc_events = {
	"Asset Request": {
		"after_insert": "frappe_it.controllers.asset_request_notifications.on_create",
		"on_update": "frappe_it.controllers.asset_request_notifications.on_update",
		"on_submit": "frappe_it.controllers.asset_request_notifications.on_submit",
	},
	"Asset Return": {
		"after_insert": "frappe_it.controllers.asset_return_notifications.on_create",
		"on_update": "frappe_it.controllers.asset_return_notifications.on_update",
		"on_submit": "frappe_it.controllers.asset_return_notifications.on_submit",
	}
}
# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "frappe_it",
# 		"logo": "/assets/frappe_it/logo.png",
# 		"title": "Frappe IT",
# 		"route": "/frappe_it",
# 		"has_permission": "frappe_it.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_it/css/frappe_it.css"
# app_include_js = "/assets/frappe_it/js/frappe_it.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_it/css/frappe_it.css"
# web_include_js = "/assets/frappe_it/js/frappe_it.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_it/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "frappe_it/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappe_it.utils.jinja_methods",
# 	"filters": "frappe_it.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_it.install.before_install"
# after_install = "frappe_it.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_it.uninstall.before_uninstall"
# after_uninstall = "frappe_it.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "frappe_it.utils.before_app_install"
# after_app_install = "frappe_it.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "frappe_it.utils.before_app_uninstall"
# after_app_uninstall = "frappe_it.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_it.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_it.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_it.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_it.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_it.tasks.weekly"
# 	],
# 	"monthly": [
# 		"frappe_it.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "frappe_it.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_it.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_it.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappe_it.utils.before_request"]
# after_request = ["frappe_it.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_it.utils.before_job"]
# after_job = ["frappe_it.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_it.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

