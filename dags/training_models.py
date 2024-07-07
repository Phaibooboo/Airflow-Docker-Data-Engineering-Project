from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from random import randint


def _training_model():
    return randint(0, 20)

def _choose_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    best_accuracy = max(accuracies) 
    if (best_accuracy > 15):
        return 'accurate' 
    return 'inaccurate'


with DAG("training_models", start_date=datetime(2024, 5, 29),
    schedule_interval="@daily", catchup=False) as dag:

# TASKS
#Training models
        training_model_A = PythonOperator(
            task_id="training_model_A",
            python_callable=_training_model
        )

        training_model_B = PythonOperator(
            task_id="training_model_B",
            python_callable=_training_model
        )

        training_model_C = PythonOperator(
            task_id="training_model_C",
            python_callable=_training_model
        )
        
        choose_best_model = BranchPythonOperator(
            task_id="choose_best_model",
            python_callable=_choose_best_model  
        )

        accurate = BashOperator(
            task_id = "accurate",
            bash_command ="echo 'accurate'"
        )

        inaccurate = BashOperator(
            task_id = "inaccurate",
            bash_command ="echo 'inaccurate'"
        )
[training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]
