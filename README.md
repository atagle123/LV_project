


<!-- ABOUT THE PROJECT -->
## About The Project
LV project to get macro and industry data from Bcentral API and from CMF chile


<!-- GETTING STARTED -->
## Getting Started


### Installation
### Conda Environment

To set up the project environment, create a Conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate lv_project
```

### Docker Setup
Build the container
```bash
docker buid -t LV_PROJECT . 
```

Run the container
```bash
docker run -it  --rm LV_PROJECT scripts/main_data.py 
```

### Setup

1. Get free API credentials at [https://si3.bcentral.cl/Siete/en/Siete/API?respuesta=](BANCO CENTRAL CHILE API)
   
2. Enter your credentials in credentials.txt in the project folder
   ```js
   USER
   PASSWORD
   ```

3. Fill the configs/empresas.json file with this format: {empresa_name : rut,...} , example: {"industry1":"94321000",...}


<!-- USAGE EXAMPLES -->
## Usage



<!-- ROADMAP -->
## File organization
```kotlin
LV_PROJECT/
│
├── data/
│   ├── industrydata/...
│   └── macrodata/...
│
├── configs/
│   └── empresas.json 
│
├── drivers/
│   └── driver1.exe
│ 
├── industry/
│   ├── data_manager.py
│   ├── html_parser.py
│   ├── industry_data.py
│   ├── parse_xbrl.py
│   ├── pdf_parser.py
│   └── scrapping.py
│
├── macro/
│   ├── get_data.py
│   ├── plots_data.py
│   └── serie.json
│
├── utils/
│   ├── cchc_preprocess.py
│   ├── download_data.py
│   ├── excel_downloads.py
│   └── json_utils.py
│  
├── scripts/
│   ├── main_data.py
│   └── reports_plots.py
│ 
├── .gitignore
├── README.md
├── credentials.txt
└── environment.yml
```


```kotlin
data/
├── industrydata/
│   ├── industry1/
│   │   ├── raw/
│   │   │   ├── html/...
│   │   │   ├── pdf_financials/...
│   │   │   ├── pdf_razonados/...
│   │   │   └── xbrl/...
│   │   │
│   │   └── results/
│   │       ├── excel/...
│   │       └── csv/...
│   │
│   └── industry2/...
│
└── macrodata/
    ├── excel/...
    └── plots/...
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




