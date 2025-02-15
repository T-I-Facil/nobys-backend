from client import get_db
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List
from pymongo.errors import PyMongoError
from schemas import Schedule

class ScheduleRepository:
    def __init__(self):
        self.db = get_db()

    def _validate_object_id(self, id_value: str) -> ObjectId:
        """
        Valida e converte um ID para ObjectId do MongoDB.
        :param id_value: ID como string.
        :return: ObjectId válido.
        """
        if not ObjectId.is_valid(id_value):
            raise ValueError(f"ID inválido: {id_value}")
        return ObjectId(id_value)

    def get_schedules(self, user_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Schedule]:
        """
        Obtém os agendamentos de um usuário com a opção de filtrar por data.

        :param user_id: ID do usuário.
        :param date: Data no formato ISO 8601 para filtrar os agendamentos.
        :return: Lista de agendamentos do usuário.
        """
        try:
            query = {"user_id": user_id}
            if start_date and end_date:
                try:
                    start_of_day = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_of_day = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
                    query["start_date"] = {"$gte": start_of_day, "$lt": end_of_day}
                except ValueError as e:
                    raise ValueError(f"Data inválida: {start_date}. Use o formato ISO 8601.") from e

            schedules_cursor = self.db.schedules.find(query)
            schedules = [
                Schedule(
                    id=str(schedule["_id"]),
                    user_id=str(schedule["user_id"]),
                    start_date=schedule["start_date"],
                    schedule_time=schedule["schedule_time"],
                    value=schedule["value"],
                    invoiced=schedule.get("invoiced", False),
                    specialty=schedule.get("specialty"),
                    description=schedule.get("description"),
                    month=schedule["start_date"].strftime("%B")
                )
                for schedule in schedules_cursor
            ]
            return schedules
        except PyMongoError as e:
            raise RuntimeError("Erro ao buscar agendamentos no banco de dados.") from e

    def add_schedule(self, user_id: str, schedule: Schedule) -> str:
        """
        Adiciona um novo agendamento ao banco de dados.

        :param schedule: Instância do modelo Schedule com os dados do agendamento.
        :return: ID do agendamento inserido.
        """
        try:
            schedule_data = schedule.model_dump()
            schedule_data["user_id"] = user_id
            result = self.db.schedules.insert_one(schedule_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise RuntimeError("Erro ao adicionar agendamento no banco de dados.") from e

    def delete_schedule(self, schedule_id: str) -> None:
        """
        Remove um agendamento do banco de dados.

        :param schedule_id: ID do agendamento a ser removido.
        """
        try:
            schedule_object_id = self._validate_object_id(schedule_id)
            result = self.db.schedules.delete_one({"_id": schedule_object_id})
            if result.deleted_count == 0:
                raise ValueError(f"Agendamento com ID {schedule_id} não encontrado.")
        except PyMongoError as e:
            raise RuntimeError("Erro ao remover agendamento do banco de dados.") from e

    def update_schedule(self, schedule_id: str, schedule: Schedule) -> None:
        """
        Atualiza um agendamento no banco de dados.

        :param schedule_id: ID do agendamento a ser atualizado.
        :param schedule: Instância do modelo Schedule com os dados atualizados.
        """
        try:
            schedule_object_id = self._validate_object_id(schedule_id)
            self.db.schedules.update_one({"_id": schedule_object_id}, {"$set": schedule})
        except PyMongoError as e:
            raise RuntimeError("Erro ao atualizar agendamento no banco de dados.") from e
        
    def get_schedule_by_id(self, schedule_id: str) -> Schedule:
        try:
            schedule_object_id = self._validate_object_id(schedule_id)
            schedule = self.db.schedules.find_one({"_id": schedule_object_id})
            if not schedule:
                raise ValueError(f"Agendamento com ID {schedule_id} não encontrado.")

            return Schedule(
                id=str(schedule["_id"]),
                user_id=str(schedule["user_id"]),
                start_date=schedule["start_date"],
                schedule_time=schedule["schedule_time"],
                value=schedule["value"],
                invoiced=schedule.get("invoiced", False),
                specialty=schedule.get("specialty"),
                description=schedule.get("description"),
            )
        except PyMongoError as e:
            raise RuntimeError("Erro ao buscar agendamento no banco de dados.") from e