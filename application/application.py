#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from flask_mail import Mail
from flask_mail import Message
from flask_sslify import SSLify
from passlib.hash import sha256_crypt
from library.functions import *

application = Flask(__name__)
application.debug = True

if (application.debug):
	# compile sass files
	import sass
	sass.compile(dirname=('static/sass', 'static/css'), output_style='compressed')
else:
	sslify = SSLify(application)

# mail config
application.config['MAIL_SERVER']= os.environ['MAIL_SERVER']
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
application.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)

application.secret_key = os.environ['SECRET_KEY']
application.domain = "LearnHub.io"
application.version = "Beta"

DEFAULT_AVATAR = os.environ['DEFAULT_AVATAR']

CLIENT = connect_to_mongodb(os.environ['MONGODB_USERNAME'], os.environ['MONGODB_PASSWORD'])
#CLIENT = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)

# define databases
DATABASE = CLIENT.test
COLLECTION_USERS = DATABASE['users']
COLLECTION_PATHWAYS = DATABASE['pathways']

# ADD GUARD FOR DATABASE CONNECTION

# ROUTES
# -----------------------------------------------------------
@application.route('/')
def index():
	'''This is the start page.'''

	if (session.get('email') == None): return redirect(url_for('logout'))

	user_id = session.get('email')

	try:
		if (get_user_account(user_id, COLLECTION_USERS) != False):
			user_account = get_user_account(user_id, COLLECTION_USERS)
			user_details = get_user_details(user_id, COLLECTION_USERS)

			# define template variables
			username = user_account["username"]
			email = user_account["email"]
			avatar = user_details["avatar"]

			# define skills and projects
			skills = get_user_skills(user_id, COLLECTION_USERS)
			projects = get_user_projects(user_id, COLLECTION_USERS)

			return render_template('index.html',
								   title=username,
								   domain=application.domain,
								   version=application.version,
								   email=email,
								   username=username,
								   avatar=avatar,
								   skills=skills,
								   projects=projects)
		else:
			# user does not exist
			return redirect(url_for('logout'))
	except:
		# general error
		return redirect(url_for('logout'))

@application.route('/profile/<username>')
def profile(username):
	'''This is the public profile page.'''

	user_id = get_user_id(username, COLLECTION_USERS)

	try:
		if (get_user_account(user_id, COLLECTION_USERS) != False):
			user_account = get_user_account(user_id, COLLECTION_USERS)
			user_details = get_user_details(user_id, COLLECTION_USERS)

			# define template variables
			username = user_account["username"]
			name = user_details["name"]
			location = user_details["location"]
			avatar = user_details["avatar"]
			facebook = user_details["facebook"]
			twitter = user_details["twitter"]
			github = user_details["github"]

			# define skills and projects
			skills = get_user_skills(user_id, COLLECTION_USERS)
			projects = get_user_projects(user_id, COLLECTION_USERS)

			return render_template('profile.html', 
							   	   title=username,
							   	   domain=application.domain,
							   	   version=application.version,
							       username=username,
							       name=name,
							       location=location,
							       avatar=avatar,
							       facebook=facebook,
							       twitter=twitter,
							       github=github,
							       skills=skills,
							       projects=projects)
		else:
			# user does not exist
			return redirect(url_for('index'))
	except:
		# general error
		return redirect(url_for('index'))

@application.route('/settings', methods=['GET', 'POST'])
def settings(title="Settings"):
	'''This is the settings page.'''

	if (session.get('email') == None): return redirect(url_for('login'))

	user_id = session.get('email')

	try:
		if (get_user_account(user_id, COLLECTION_USERS) != False):
			user_account = get_user_account(user_id, COLLECTION_USERS)
			user_details = get_user_details(user_id, COLLECTION_USERS)

			# define password
			password = user_account["password"]

			# define template variables
			username = user_account["username"]
			email = user_account["email"]
			name = user_details["name"]
			location = user_details["location"]
			avatar = user_details["avatar"]
			facebook = user_details["facebook"]
			twitter = user_details["twitter"]
			github = user_details["github"]

			# default avatar
			if (avatar == DEFAULT_AVATAR):
				avatar = False

			# change password
			if ('change_password_submit' in request.form):
				new_password = sha256_crypt.encrypt(request.form['password_update_new_first'])

				if (sha256_crypt.verify(request.form['password_update_current'], password)):
					if (change_password(new_password, user_id, COLLECTION_USERS) == True):
						flash(u"Successfully changed password", "success")
						return redirect(url_for('settings'))
					else:
						flash(u"Something went wrong", "error")
						return redirect(url_for('settings'))

				else:
					flash(u"Passwords did not match", "error")
					return redirect(url_for('settings'))

			# delete account
			if ('delete_account_submit' in request.form):
				if (sha256_crypt.verify(request.form['delete_account_password'], password)):
					if (delete_account(user_id, COLLECTION_USERS) == True):
						flash(u"Successfully deleted account", "success")
						return redirect(url_for('logout'))
					else:
						flash(u"Something went wrong", "error")
						return redirect(url_for('settings'))

				else:
					flash(u"Wrong password.", "error")
					return redirect(url_for('settings'))

			return render_template('settings.html',
					 			   title=title,
					 			   domain=application.domain,
					 			   version=application.version,
					 			   email=email,
					 			   username=username,
					 			   name=name,
					 			   location=location,
					 			   avatar=avatar,
					 			   facebook=facebook,
					 			   twitter=twitter,
					 			   github=github)
		else:
			# user does not exist
			return redirect(url_for('logout'))
	except:
		# general error
		return redirect(url_for('index'))

@application.route('/explore', methods=['GET', 'POST'])
def explore():
	'''This is the explore page.'''

	user_id = session.get('email')

	try:
		# define user details (if logged in)
		if (get_user_account(user_id, COLLECTION_USERS) != False):
			user_account = get_user_account(user_id, COLLECTION_USERS)
			username = user_account["username"]
			email = user_account["email"]
			password = user_account["password"]
		else:
			username = False
			email = False
			password = False

		# get pathways
		pathways = get_pathways(COLLECTION_PATHWAYS)

		# delete pathway
		if ('delete_pathway_submit' in request.form):
			# get pathway id and owner
			pathway_id = request.form['delete_pathway_id']
			pathway_owner = get_pathway_owner(pathway_id, COLLECTION_PATHWAYS)

			# check that user is owner
			if (username == pathway_owner):
				# check password
				if (sha256_crypt.verify(request.form['delete_pathway_password'], password)):
					if (delete_pathway(pathway_id, COLLECTION_PATHWAYS) == True):
						flash(u"Successfully deleted pathway", "success")
						return redirect(url_for('explore'))
					else:
						flash(u"Something went wrong", "error")
						return redirect(url_for('explore'))
				else:
					flash(u"Wrong password.", "error")
					return redirect(url_for('explore'))
			else:
				flash(u"You are not owner.", "error")
				return redirect(url_for('explore'))

		return render_template('explore.html',
							   title="Explore",
							   domain=application.domain,
							   version=application.version,
							   email=email,
							   username=username,
							   pathways=pathways)

	except Exception as e:
		# general error
		flash(e)
		return redirect(url_for('logout'))

@application.route('/login', methods=['GET', 'POST'])
def login(title="Login"):
	'''This is the login page.'''

	if (session.get('email') != None): return redirect(url_for('index'))

	# login
	if ('login_submit' in request.form):
		login_email = request.form['login_email']

		if (get_user_account(login_email, COLLECTION_USERS) == False):
			flash(u"Wrong email or password.", "error")
			return redirect(url_for('login'))

		else:
			try:
				user_account = get_user_account(login_email, COLLECTION_USERS)
				password = user_account["password"]

				if (sha256_crypt.verify(request.form['login_password'], password)):
					session['email'] = login_email

					return redirect(url_for('index'))

				else:
					flash("Wrong email or password.")
					return redirect(url_for('login'))
			except:
				# something went wrong
				return redirect(url_for('logout'))

	# create new
	if ('create_submit' in request.form):
		create_email = request.form['create_email']

		if (create_email != ""):
			if (get_user_account(create_email, COLLECTION_USERS) == False):
				session['email'] = create_email

				return redirect(url_for('create'))

			else:
				flash(u"This email is already used.", "error")
				return redirect(url_for('login'))
		else:
			flash(u"Invalid email.", "error")
			return redirect(url_for('login'))

	# reset password
	if ('reset_password_submit' in request.form):
		reset_email = request.form['reset_password_email']

		if (get_user_account(reset_email, COLLECTION_USERS) == False):
			flash(u"This email does not exist.", "error")
			return redirect(url_for('login'))

		else:
			try:
				# generate new password
				password_plain = generate_password()
				password_encrypted = sha256_crypt.encrypt(password_plain)

				# create email
				reset_password_mail = Message("Hi there!",
											  body="Here's your new password: " + password_plain, 
					 						  sender="support@letslearn.io",
					 						  recipients=[reset_email])

				# change to new password and send email
				if (change_password(password_encrypted, reset_email, COLLECTION_USERS) == True):
					mail.send(reset_password_mail)
					flash(u"New password sent to email.", "success")
					return redirect(url_for('login')) 
				else:
					flash(u"Something went wrong", "error")
					return redirect(url_for('login'))

			except:
				# something went wrong
				return redirect(url_for('logout'))

	return render_template('login.html', 
						   title=title,
						   domain=application.domain,
						   version=application.version)

@application.route('/create', methods=['GET', 'POST'])
def create(title="Create new"):
	'''This is the create new page.'''

	if (session.get('email') == None): return redirect(url_for('logout'))

	email = session.get('email')

	# create new
	if ('create_new_submit' in request.form):
		username = request.form['create_new_username'].lower()
		password = sha256_crypt.encrypt(request.form['create_new_password'])

		if (user_exists(username, COLLECTION_USERS) == False):
			if (create_new_user(username, password, email, DEFAULT_AVATAR, COLLECTION_USERS) == True):
				return redirect(url_for('index'))

			else:
				flash(u"Something went wrong.", "error")
				return redirect(url_for('login'))

		else:
			flash(u"This username is already used.", "error")

			return redirect(url_for('create'))

	return render_template('create.html',
						   title=title,
						   domain=application.domain,
						   version=application.version,
						   email=email)

@application.route('/logout')
def logout(title="Logout"):
	'''This is the logout page.'''

	session.clear()

	return redirect(url_for('login'))

@application.errorhandler(404)
def page_not_found(error, title="Page not found"):
	'''This is the error page.'''

	return redirect(url_for('login'))

	#return render_template('404.html', title=title), 404

# AJAX
# -----------------------------------------------------------
@application.route('/_add_skill')
def add_skill():
	'''AJAX add skill.'''

	user_id = session.get('email')

	# define skill
	skill_name = request.args.get('skill_name').strip()
	skill_level = request.args.get('skill_level')

	# check skills
	skills = get_user_skills(user_id, COLLECTION_USERS)
	if (skills != False):
		for skill in skills:
			if (skill_name.lower() == skill['skill_name'].lower()):
				return jsonify(response=-1)

	if ((user_id != None) and (skill_name.lower() != "")):
		skill_id = add_skill_for_user(user_id, skill_name, skill_level, COLLECTION_USERS)
		if (skill_id):
			return jsonify(response=skill_id)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=False)

@application.route('/_delete_skill')
def delete_skill():
	'''AJAX delete skill.'''

	user_id = session.get('email')

	skill_id = request.args.get('skill_id')

	if (user_id != None):
		if (delete_skill_for_user(user_id, skill_id, COLLECTION_USERS) == True):
			return jsonify(response=True)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=False)

@application.route('/_add_project')
def add_project():
	'''AJAX add project.'''

	user_id = session.get('email')
	skills = get_user_skills(user_id, COLLECTION_USERS)

	# define project
	project_name = request.args.get('project_name').strip()
	project_description = request.args.get('project_description').strip()
	project_link = request.args.get('project_link').strip()
	project_skills = request.args.get('project_skills')

	# iterate and get skill names from skill_id
	skill_list = []
	for project_skill in project_skills.split(','):
		for skill in skills:
			if (project_skill == skill['skill_id']):
				skill_list.append(skill['skill_name'])

	# check project name
	projects = get_user_projects(user_id, COLLECTION_USERS)
	if (projects != False):
		for project in projects:
			if (project_name.lower() == project['project_name'].lower()):
				return jsonify(response=-1)

	# add project for user
	if ((user_id != None) and (project_name.lower() != "")):
		project_id = add_project_for_user(user_id, project_name, project_description, project_link, skill_list, COLLECTION_USERS)
		if (project_id):
			return jsonify(response=project_id)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=False)

	return jsonify(response=True)

@application.route('/_delete_project')
def delete_project():
	'''AJAX delete project.'''

	user_id = session.get('email')

	project_id = request.args.get('project_id')

	if (user_id != None):
		if (delete_project_for_user(user_id, project_id, COLLECTION_USERS) == True):
			return jsonify(response=True)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=False)

@application.route('/_account_update_username')
def account_update_username():
	user_id = session.get('email')
	new_username = request.args.get('account_update_username').lower().strip()

	# user_exists
	if (user_exists(new_username, COLLECTION_USERS) == False):
		# update_username
		if (update_username(new_username, user_id, COLLECTION_USERS) == True):
			return jsonify(response=True)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=-1)

@application.route('/_account_update_name')
def account_update_name():
	user_id = session.get('email')
	new_name = request.args.get('account_update_name').strip()

	# update_name
	if (update_name(new_name, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_update_location')
def account_update_location():
	user_id = session.get('email')
	new_location = request.args.get('account_update_location').strip()

	# update_location
	if (update_location(new_location, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_update_avatar', methods=['GET', 'POST'])
def account_update_avatar():
	user_id = session.get('email')
	# new_avatar = request.args.get('account_update_avatar')
	new_avatar = request.json

	# update_avatar
	if (update_avatar(new_avatar, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_update_facebook')
def account_update_facebook():
	user_id = session.get('email')
	new_facebook = request.args.get('account_update_facebook').lower().strip()

	# update_facebook
	if (update_facebook(new_facebook, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_update_twitter')
def account_update_twitter():
	user_id = session.get('email')
	new_twitter = request.args.get('account_update_twitter').strip()

	# update_twitter
	if (update_twitter(new_twitter, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_update_github')
def account_update_github():
	user_id = session.get('email')
	new_github = request.args.get('account_update_github').strip()

	# update_github
	if (update_github(new_github, user_id, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_account_remove_avatar')
def account_remove_avatar():
	user_id = session.get('email')

	# remove_avatar
	if (remove_avatar(user_id, DEFAULT_AVATAR, COLLECTION_USERS) == True):
		return jsonify(response=True)
	else:
		return jsonify(response=False)

@application.route('/_create_new_pathway')
def create_new_pathway():
	user_id = session.get('email')
	user_account = get_user_account(user_id, COLLECTION_USERS)

	# define user details
	username = user_account["username"]

	# define pathway details
	pathway_name = request.args.get('pathway_name').strip()
	pathway_level = request.args.get('pathway_level')
	pathway_tags = request.args.get('pathway_tags')

	# iterate and add pathway tags to list
	tag_list = []
	for tag in pathway_tags.split(','):
		tag_list.append(tag)

	# append pathway level as tag
	tag_list.append(pathway_level)

	if ((pathway_name != None) and (pathway_name != "") and (pathway_name != False)):
		pathway_id = create_pathway(username, pathway_name, pathway_level, tag_list, COLLECTION_PATHWAYS)
		if (pathway_id):
			return jsonify(response=pathway_id)
		else:
			return jsonify(response=False)
	else:
		return jsonify(response=-1)

@application.route('/_add_resource')
def add_resource():
	user_id = session.get('email')
	user_account = get_user_account(user_id, COLLECTION_USERS)

	# define user details
	username = user_account["username"]

	# define pathway
	pathway_id = request.args.get('pathway_id')
	pathway_owner = get_pathway_owner(pathway_id, COLLECTION_PATHWAYS)

	if (username == pathway_owner):
		# define resource details
		resource_name = request.args.get('resource_name')
		resource_link = request.args.get('resource_link')
		resource_type = request.args.get('resource_type')

		if ((resource_name != None) and (resource_name != "") and (resource_name != False)):
			if (add_resource_for_pathway(pathway_id, resource_name, resource_link, resource_type, COLLECTION_PATHWAYS)):
				return jsonify(response=True)
			else:
				return jsonify(response=False)
		else:
			return jsonify(response=-1)
	else:
		return jsonify(response=-2)

@application.route('/_delete_resource')
def delete_resource():
	'''Delete resource for pathway.'''
	user_id = session.get('email')
	user_account = get_user_account(user_id, COLLECTION_USERS)

	# define user details
	username = user_account["username"]

	# define pathway
	pathway_id = request.args.get('pathway_id')
	pathway_owner = get_pathway_owner(pathway_id, COLLECTION_PATHWAYS)

	if (username == pathway_owner):
		# define resource to delete
		resource_id = request.args.get('resource_id')

		if ((resource_id != None) and (resource_id != False)):
			if (delete_resource_for_pathway(pathway_id, resource_id, COLLECTION_PATHWAYS)):
				return jsonify(response=True)
			else:
				return jsonify(response=False)
		else:
			return jsonify(response=-1)
	else:
		return jsonify(response=-2)

@application.route('/_pathway_resources')
def pathway_resources():
	'''API to get pathway resources.'''

	pathway_id = request.args.get('pathway_id')

	pathway_resources = get_pathway_resources(pathway_id, COLLECTION_PATHWAYS)
	if (pathway_resources):
		return jsonify(response=pathway_resources)
	else:
		return jsonify(response=False)

# -----------------------------------------------------------
if __name__ == '__main__':
	application.run(threaded = True)
