How to Run the Project

Steps:

1. **Install Docker Desktop**
   - Make sure you have Docker Desktop installed on your system.
   - Ensure that WSL2 is installed and set as the default backend.

2. **Clone the Project from GitHub**
   - Clone the repository to your local machine using:
     git clone <repository-url>

3. **Open WSL**
   - Launch Command Prompt (CMD) and type:
     wsl

4. **Navigate to the Project Directory**
   - Use the `cd` command to go to the project folder, for example:
     cd "/mnt/c/Users/<your-username>/path/to/project"

5. **Verify docker-compose.yml Exists**
   - Make sure the file `docker-compose.yml` is in the root of the project directory.

6. **Run the Project Using Docker Compose**
   - In the same directory, run the following command:
     docker-compose up --build

7. **Access the Application**
   - After the build finishes, the app will be running in a Docker container.
   - Open your browser and go to:
     http://localhost:<port>
   - Replace `<port>` with the correct port defined in the docker-compose.yml file.
