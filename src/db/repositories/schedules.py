from db.client import get_db
from ..schemas import Schedule
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List
from pymongo.errors import PyMongoError


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

    def get_schedules(self, user_id: str, date: Optional[str] = None) -> List[Schedule]:
        """
        Obtém os agendamentos de um usuário com a opção de filtrar por data.

        :param user_id: ID do usuário.
        :param date: Data no formato YYYY-MM-DD para filtrar os agendamentos.
        :return: Lista de agendamentos do usuário.
        """
        try:
            query = {"user_id": user_id}
            if date:
                try:
                    start_of_day = datetime.strptime(date, "%Y-%m-%d")
                    end_of_day = start_of_day + timedelta(days=1)
                    query["start_date"] = {"$gte": start_of_day, "$lt": end_of_day}
                except ValueError as e:
                    raise ValueError(f"Data inválida: {date}. Use o formato YYYY-MM-DD.") from e

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
