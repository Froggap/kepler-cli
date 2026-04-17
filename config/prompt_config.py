import os
from dotenv import load_dotenv

load_dotenv()

class ReportConfig:
    COMPANY_NAME  = os.getenv("COMPANY_NAME") or "Empresa"
    EMPLOYEE_NAME = os.getenv("EMPLOYEE_NAME") or "Colaborador" # de hecho ya saca el nombre del autor del commit, pero por si acaso
    PROJECT_NAME  = os.getenv("PROJECT_NAME") or "Proyecto" # de hecho ya saca el nombre del proyecto, pero por si acaso, pero si lo quieres estatico...
    "... idk xd"