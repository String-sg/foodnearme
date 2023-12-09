# Food Near Me
Find nearby food by inputting a postal code
<img width="944" alt="image" src="https://github.com/String-sg/foodnearme/assets/44336310/d5738abd-8e62-4d93-9ef9-ca04b37585a0">

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
1) Making API calls (Google Places)
2) Deploying to web (Streamlit)
3) Connecting to a backend (CockroachDB)/ Implementing a review system
4) Using a ORM/ SQLalchemy (in progress)
