## Run Pipeline transform with Spark

To run the demo do the following steps:

- Create and activate python virtual environment
- Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
````
- Set the Hugging Face token as environment variable: 
```bash
HF_TOKEN=<TOKEN>
```
- Run the demo script: `python` [`pipeline_local_fork_demo.py`](./src/data_processing/examples/pipeline/spark/pipeline_local_fork_demo.py)
- To view the results, run:
`python` [`show-results.py`](./src/data_processing/examples/pipeline/spark/show-results.py)