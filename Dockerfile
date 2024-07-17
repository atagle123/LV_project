# Use the Miniconda3 base image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /LV_PROJECT

# Copy the environment.yml file into the container
COPY environment.yml .
COPY .  /LV_PROJECT/
# Create the environment from the yml file
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "lv_project", "/bin/bash", "-c"]

# Copy the rest of your application code

# Set the entrypoint to your script
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "lv_project", "python", "scripts/main_data.py"]
