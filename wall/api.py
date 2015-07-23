from flask import Blueprint, render_template, abort, jsonify, request
from wall import app, db, models
from operator import itemgetter
import datetime

wall_api = Blueprint('wall_api', __name__, url_prefix='/api/v1')

import datetime
import json

@wall_api.route("/ci/<int:build_id>", methods=["GET"])
@wall_api.route("/ci", methods=["GET"])
def get_ci(build_id=None):
	if build_id is None:
		pendingList = models.ContinuousBuilds.query.filter_by(phase="STARTED")
		completedList = models.ContinuousBuilds.query.filter_by(phase="FINALIZED").order_by(models.ContinuousBuilds.number.desc())[:10]
		buildList =[]
		for pending in pendingList:
			buildList.append(pending.as_dict())
		for completed in completedList:
			buildList.append(completed.as_dict())

		buildList = sorted(buildList, key=itemgetter('number'))
	elif models.ContinuousBuilds.query.get(build_id) is None:
		return jsonify({'success': False, 'msg': 'User ' + str(build_id) + ' not found'}), 400
	else:
		build = models.ContinuousBuilds.query.get(build_id)
		return jsonify(build.as_dict())

	return jsonify(builds=buildList)


@wall_api.route("/ci", methods=["POST"])
def post_ci():
	""" Add the specified ci 
	{
	    "name": "asgard",
	    "url": "job/asgard/",
	    "build": {
	        "full_url": "http://localhost:8080/job/asgard/18/",
	        "number": 18,
	        "phase": "COMPLETED",
	        "status": "SUCCESS",
	        "url": "job/asgard/18/",
	        "scm": {
	            "url": "https://github.com/evgeny-goldin/asgard.git",
	            "branch": "origin/master",
	            "commit": "c6d86dc654b12425e706bcf951adfe5a8627a517"
	        },
	        "parameters": {
	        	"gitlabSourceBranch": "pilot",
	        	"gitlabTargetBranch": "master"
	        },
	        "artifacts": {
	            "asgard.war": {
	                "archive": "http://localhost:8080/job/asgard/18/artifact/asgard.war"
	            },
	            "asgard-standalone.jar": {
	                "archive": "http://localhost:8080/job/asgard/18/artifact/asgard-standalone.jar",
	                "s3": "https://s3-eu-west-1.amazonaws.com/evgenyg-bakery/asgard/asgard-standalone.jar"
	            }
	        }
    	}
	}
	"""
	parameters = json.loads(request.data)
	if 'build' in parameters:
		name = parameters['name']
		build = parameters['build']

		if models.ContinuousBuilds.query.filter_by(number=int(build['number'])).first() is None:
			newBuild = models.ContinuousBuilds(
				name = name,
			    number = int(build['number']),
			    phase =  build['phase'],
			    status = "RUNNING",
			    sourceBranch =  build['parameters']['gitlabSourceBranch'],
			    targetBranch = build['parameters']['gitlabTargetBranch'],
			    full_url = build['full_url'],
			    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			    )
			db.session.add(newBuild)
			db.session.commit()
			return jsonify({'success': True, 'msg': 'ack'}), 200
		else:
			existBuild = models.ContinuousBuilds.query.filter_by(number=int(build['number'])).first()
			if existBuild.phase == build['phase']:
				return jsonify({'success': False, 'msg': 'Already got this one matey'}), 400
			else:
				existBuild.phase = build['phase']
				existBuild.status = build['status']
				existBuild.date_modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				db.session.commit()
				return jsonify({'success': True, 'msg': 'ack'}), 200

	else:
		return jsonify({'success': False, 'msg': 'No build specified'}), 400


@wall_api.route("/deploy/<int:deploy_id>", methods=["GET"])
@wall_api.route("/deploy", methods=["GET"])
def get_deploy(deploy_id=None):
	if deploy_id is None:
		deployList = models.Deployments.query.all()
	elif models.Deployments.query.get(deploy_id) is None:
		return jsonify({'success': False, 'msg': 'User ' + str(deploy_id) + ' not found'}), 400
	else:
		deploy = models.Deployments.query.get(deploy_id)
		return jsonify(deploy.as_dict())

	return jsonify(deploys=[i.as_dict() for i in deployList])


@wall_api.route("/deploy", methods=["POST"])
def post_deploy():
	parameters = json.loads(request.data)
	if 'build' in parameters:
		name = parameters['name']
		print name
		build = parameters['build']

		if models.Deployments.query.filter_by(name=name).first() is None:
			newDeploy = models.Deployments(
				name = name,
			    number = int(build['number']),
			    phase =  build['phase'],
			    status = "RUNNING",
			    sourceBranch =  build['parameters']['gitlabSourceBranch'],
			    full_url = build['full_url'],
			    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			    )
			db.session.add(newDeploy)
			db.session.commit()
			return jsonify({'success': True, 'msg': 'ack'}), 200
		else:
			existDeploy = models.Deployments.query.filter_by(name=name).first()
			if existDeploy.phase == build['phase']:
				return jsonify({'success': False, 'msg': 'Already got this one mate'}), 400
			else:
                try:
                    build['status']
                except NameError:
                    build['status'] = "RUNNING"
				existDeploy.phase = build['phase']
				existDeploy.status = build['status']
				existDeploy.number = int(build['number'])
				existDeploy.date_modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				db.session.commit()
				return jsonify({'success': True, 'msg': 'ack'}), 200

	else:
		return jsonify({'success': False, 'msg': 'No build specified'}), 400
