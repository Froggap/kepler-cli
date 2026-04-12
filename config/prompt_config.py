import os
from dotenv import load_dotenv

load_dotenv()

class ReportConfig:
    COMPANY_NAME  = os.getenv("COMPANY_NAME", "Empresa")
    EMPLOYEE_NAME = os.getenv("EMPLOYEE_NAME", "Colaborador") # de hecho ya saca el nombre del autor del commit, pero por si acaso
    PROJECT_NAME  = os.getenv("PROJECT_NAME", "Proyecto") # de hecho ya saca el nombre del proyecto, pero por si acaso, pero si lo quieres estatico...
    "... idk xd"