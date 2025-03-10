🏆 PadelMaster - Configuración con Docker Desktop
Este proyecto utiliza Docker para ejecutar el backend y frontend en contenedores, facilitando su despliegue y ejecución.

Antes de empezar, asegúrate de tener instalado Docker Desktop.

🌐 Creación de la red de Docker
Para que el backend y el frontend puedan comunicarse de manera segura, primero debemos crear una red de Docker compartida:
docker network create padelmaster-network

⚙️ Construcción y ejecución
🖥️ Backend
Para construir y ejecutar el backend en Docker, ejecuta los siguientes comandos:
docker stop padelmaster-backend-container
docker rm padelmaster-backend-container
docker build -t padelmaster-backend .
docker run -d --name padelmaster-backend-container --network padelmaster-network -p 8000:8000 padelmaster-backend

🎨 Frontend
Para construir y ejecutar el frontend en Docker, usa estos comandos:
docker stop padelmaster-frontend-container
docker rm padelmaster-frontend-container
docker build -t padelmaster-frontend .
docker run -d --name padelmaster-frontend-container --network padelmaster-network -p 8501:8501 padelmaster-frontend

✅ Verificación de funcionamiento
Para comprobar que todo está funcionando correctamente, sigue estos pasos:

1️⃣ Ejecutar el backend:
uvicorn main:app --reload

2️⃣ Ejecutar el frontend:
streamlit run src/app.py
Esto abrirá directamente en el navegador predeterminado la aplicación.

⏹️ Detener y eliminar los contenedores
Si necesitas detener y eliminar ambos contenedores, ejecuta:
docker stop padelmaster-backend-container padelmaster-frontend-container
docker rm padelmaster-backend-container padelmaster-frontend-container
