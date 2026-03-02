from celery.result import AsyncResult
from flask_restx import Resource

from app import celery
from app.api import api

namespace = api.namespace(
    name="tasks",
    description="fetch progress and results for deferred tasks"
)


@namespace.route("/<task_id>")
class TasksAPI(Resource):
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)

        response = {
            "id": task_id,
            "state": task.state,
            "current": None,
            "total": None,
            "status": None,
            "result": None,
        }

        if task.state == "PENDING":
            response["status"] = "waiting for worker"

        elif task.state != "FAILURE":
            response["current"] = task.info.get("current", 0.0)
            response["status"] = task.info.get("status")
            response["result"] = task.info.get("result")

        else:
            response["current"] = 0.0
            response["total"] = 1.0
            response["status"] = str(task.info)

        return response
