Deployed Endpoints:

        HTML Mode   : https://mc-simple-req.herokuapp.com/home
        GET Mode    : https://mc-simple-req.herokuapp.com/lotarea/values
        POST mode   : curl --location --request POST 'https://mc-simple-req.herokuapp.com/get-stats/api' --data-raw '{ "column": "alley", "method": "common" }

Environment configuration:

        The API is deployed in Heroku using the gunicorn WSGI framework. The Procfile contains the initialisation script for the gunicorn env. For cross 
        environmental deployments please ensure to change the config_file.py and the requirements.txt with the necessary python modules. The config_file.py 
        has been gitignored for this very reason 

Api works on three modes: 

    1.  HTML Interface
        The HTML interface is a readily available tool to validate columns and their respective results. Only the columns available in the data set/data description 
        would be available for fetching. The landing page for the interface is at `env:<port>/home` for eg `http://localhost:5000/home`. The results are displayed
        in the `env:<port>/get_stats_results` page. For optimal results always clear cache before loading. Do not use the `env:<port>/get_stats_results` as a landing 
        page , since the results are dynamically generated from the home page. Both invalid columns and blank column names result in the 'Invalid column name' error
        As of now only options for fetch are unique values and common values.

    2.  GET mode
        Fetch the results of the either the most values count (values) or common records (common). Endpoint for this mode is `env:<port>/get-stats/<colname>/<method>` 
        for eg  `http://localhost:5000/get-stats/lotarea/values`. As with the HTML interface only column names which are available in the data set should be supplied
        Invalid requests will get warnings in return

    3.  POST mode
        Although this is in POST mode the only difference with the above is the request body. Endpoint for this mode is `env:<port>/get-stats/api` 
        for eg  `http://localhost:5000/get-stats/api` . The request body should be supplied as JSON in the format { "column": "MSZoning", "method": "values" }
        where column name is available in the data set and methods should be either the most values count (values) or common records (common). Sample request 
        should look like `curl --location --request POST 'http://localhost:5000/get-stats/api' --data-raw '{ "column": "alley", "method": "common" }'`


