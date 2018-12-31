#!/usr/bin/python

import os
import random
import string
import uuid
import sys
import pymongo
import requests
import xlsxwriter
import dns

from datetime import datetime
from datetime import timedelta
from lxml import etree

def connect_to_mongodb(USERNAME, PASSWORD):
    '''Function to connect to MongoDB hosted database.'''

    try:
        return pymongo.MongoClient("mongodb+srv://" + USERNAME + ":" + PASSWORD + "@cluster0-29i1l.mongodb.net/test?retryWrites=true")
    
    except:
        return False

def user_exists(username, DB):
	'''Check if username already exists in database.'''
	if (DB.find_one({"username": username}) != None):
		return True

	else:
		return False

def get_user_id(username, DB):
	'''Get user id for username in database.'''

	try:
		user_id = DB.find_one({"username": username})['_id']

		if (user_id != None):
			return user_id

		else:
			return False
	except:
		return False

def get_user_account(user_id, DB):
	'''Get user account.'''

	user = DB.find_one({"_id": user_id})

	if (user != None):
		user_account = {
			"username": user["username"],
			"password": user["password"],
			"email": user["email"],
			"created": user["created"]
		}

		return user_account

	else:
		return False

def get_user_details(user_id, DB):
	'''Get user profile.'''

	user = DB.find_one({"_id": user_id})

	if (user != None):
		user_details = {
			"name": user["name"],
			"location": user["location"],
			"avatar": user["avatar"],
			"facebook": user["facebook"],
			"twitter": user["twitter"],
			"github": user["github"]
		}

		return user_details


	else:
		return False

def get_user_skills(user_id, DB):
	'''Get user skills.'''

	user = DB.find_one({"_id": user_id})

	if (user != None):
		try:
			skills = user["skills"]

			return skills

		except:
			return False

	else:
		return False

def get_user_projects(user_id, DB):
	'''Get user projects.'''

	user = DB.find_one({"_id": user_id})

	if (user != None):
		try:
			projects = user["projects"]

			return projects

		except:
			return False

	else:
		return False

def create_new_user(username, password, email, avatar, DB):
	''''Create new user.'''

	user = {"_id": email}
	DB.insert_one(user)

	try:
		DB.update_one(
			{"_id": email}, {"$set": {
				"username": username,
				"password": password,
				"email": email,
				"created": str(datetime.now()),
				"name": False,
				"location": False,
				"avatar": avatar,
				"facebook": False,
				"twitter": False,
				"github": False
			}
		})

		return True

	except:
		return False

def update_username(new_username, user_id, DB):
	'''Update username.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"username": new_username
			}
		})

		return True

	except:
		return False

def update_name(new_name, user_id, DB):
	'''Update name.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"name": new_name
			}
		})

		return True

	except:
		return False

def update_location(new_location, user_id, DB):
	'''Update location.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"location": new_location
			}
		})

		return True

	except:
		return False

def update_avatar(new_avatar, user_id, DB):
	'''Update avatar.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"avatar": new_avatar
			}
		})

		return True

	except:
		return False

def update_facebook(new_facebook, user_id, DB):
	'''Update facebook.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"facebook": new_facebook
			}
		})

		return True

	except:
		return False

def update_twitter(new_twitter, user_id, DB):
	'''Update twitter.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"twitter": new_twitter
			}
		})

		return True
		
	except:
		return False

def update_github(new_github, user_id, DB):
	'''Update github.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"github": new_github
			}
		})

		return True
		
	except:
		return False

def remove_avatar(user_id, DEFAULT_AVATAR, DB):
	'''Remove avatar and set default.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"avatar": DEFAULT_AVATAR
			}
		})

		return True
		
	except:
		return False

def generate_password():
	'''Generate random password.'''

	password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

	return password

def change_password(new_password, user_id, DB):
	'''Change password.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$set": {
				"password": new_password
			}
		})

		return True

	except:
		return False

def delete_account(user_id, DB):
	'''Delete account.'''

	try:
		DB.remove({"_id": user_id})

		return True

	except:
		return False

def add_skill_for_user(user_id, skill_name, skill_level, DB):
	'''Add skill'''

	skill_id = str(uuid.uuid4())

	try:
		DB.update_one({"_id": user_id}, {"$push": {"skills": {
			"skill_id": skill_id,
			"skill_name": skill_name,
			"skill_level": skill_level
		}}})

		return skill_id

	except:
		return False

def delete_skill_for_user(user_id, skill_id, DB):
	'''Delete skill'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$pull": {"skills": {
		 		"skill_id": skill_id
		}}})

		return True

	except:
		return False

def add_project_for_user(user_id, project_name, project_description, project_link, project_skills, DB):
	'''Add project.'''

	project_id = str(uuid.uuid4())

	try:
		DB.update_one({"_id": user_id}, {"$push": {"projects": {
			"project_id": project_id,
			"project_name": project_name,
			"project_description": project_description,
			"project_link": project_link,
			"project_skills": project_skills
		}}})

		return project_id

	except:
		return False

def delete_project_for_user(user_id, project_id, DB):
	'''Delete project.'''

	try:
		DB.update_one(
			{"_id": user_id}, {"$pull": {"projects": {
		 		"project_id": project_id
		}}})

		return True

	except:
		return False

def get_pathways(DB):
	'''Get pathways.'''

	pathways = DB.find({})

	if (pathways != None):
		return pathways

	else:
		return False

def create_pathway(username, pathway_name, pathway_level, pathway_tags, DB):
	'''Create new pathway.'''

	# generate unique pathway id
	pathway_id = str(uuid.uuid4())

	# insert pathway
	pathway = {"_id": pathway_id}
	DB.insert_one(pathway)

	try:
		DB.update_one({"_id": pathway_id}, {"$set": {
			"owner": username,
			"name": pathway_name,
			"tags": pathway_tags
		}})

		return pathway_id

	except:
		return False

def add_resource_for_pathway(pathway_id, resource_name, resource_link, resource_type, DB):
	'''Add resource to pathway.'''

	resource_id = str(uuid.uuid4())

	try:
		DB.update_one({"_id": pathway_id}, {"$push": {"resources": {
			"resource_id": resource_id,
			"name": resource_name,
			"link": resource_link,
			"type": resource_type
		}}})

		return True

	except:
		return False

def delete_resource_for_pathway(pathway_id, resource_id, DB):
	'''Delete resource.'''

	try:
		DB.update_one(
			{"_id": pathway_id}, {"$pull": {"resources": {
		 		"resource_id": resource_id
		}}})

		return True

	except:
		return False

def get_pathway_owner(pathway_id, DB):
	'''Get pathway owner.'''

	try:
		owner = DB.find_one({"_id": pathway_id})['owner']

		if (owner != None):
			return owner

		else:
			return False
	except:
		return False

def get_pathway_resources(pathway_id, DB):
	'''Get pathway resources.'''

	try:
		resources = DB.find_one({"_id": pathway_id})['resources']

		if (resources != None):
			return resources

		else:
			return False
	except:
		return False

def delete_pathway(pathway_id, DB):
	'''Delete pathway.'''

	try:
		DB.remove({"_id": pathway_id})

		return True

	except:
		return False

# ----------------------------------------- #
