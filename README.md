# Food Near Me
Find nearby food by inputting a postal code
![image](https://github.com/String-sg/foodnearme/assets/44336310/dfddde7c-8d7c-41bb-a859-e3b18b10b08e)

### To setup locally
- Clone the repository
- Go to the folder of your choice and run this command in the terminal
```git clone {top right corner}```
- To start:
```streamlit run app.py```
If you get error messages, please ensure that the necessary python packages and streamlit are installed

You will also need a Google Places API key and also add that file secrets.toml to a folder called .streamlit nested in the root directory 

### To deploy on web
See instructions on [streamlit](https://streamlit.io/cloud)

### Notes and known issues
- No backend
- Sometimes non-restaurant entries are shown

### Why this repo exists?
Prepared for OGP mentorship as a way to explain:
[x] 1) Making API calls (Google Places)
[x] 2) Deploying to web (Streamlit)
[x] 3) Connecting to a backend (CockroachDB)/ Implementing a review system
4) Using a ORM/ SQLalchemy (in progress)
