from pyrebase import pyrebase

config = {
    "apiKey": "your apiKey",
    "authDomain": "your authDomain",
    "databaseURL": "your databaseURL",
    "projectId": "your projectId",
    "storageBucket": "your storageBucket",
    "messagingSenderId": "your messagingSenderId",
    "appId": "your appId"
  };


# initialize app with config
firebase = pyrebase.initialize_app(config)













'''

<!-- The core Firebase JS SDK is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/7.8.2/firebase-app.js"></script>

<!-- TODO: Add SDKs for Firebase products that you want to use
     https://firebase.google.com/docs/web/setup#available-libraries -->

<script>
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyDUpMOheKfDndBnDE0YmPhKIdSW1L8yvBc",
    authDomain: "socialconnection-cd010.firebaseapp.com",
    databaseURL: "https://socialconnection-cd010.firebaseio.com",
    projectId: "socialconnection-cd010",
    storageBucket: "socialconnection-cd010.appspot.com",
    messagingSenderId: "1028608371475",
    appId: "1:1028608371475:web:4f2c2af814e14dc7a748e6"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
</script>


'''
