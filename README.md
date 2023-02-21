# SINGRA Platform

create and manage online courses, assessments, and learning resources in one place. Our platform provides a user-friendly interface that enables trainers to design and deliver high-quality online learning experiences to their learners. SINGRA offers a wide range of tools and resources to support the entire education process, from curriculum development to student assessment. Our robust quiz feature helps learners test their knowledge and provides valuable feedback to trainers. With SINGRA, you can easily collaborate with other trainers and educators to enhance the quality of your education delivery. Join us today and experience the power of SINGRA!

## Installation

### Flask-App-Hosted-On-VPS

Files needed to host a flask application on a linux VPS.

#### Commands

#### Install Python and Pip

Run the following commands on the VPS.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install flask.

```bash
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install venv
```
#### Create and activate the venv

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Update .env file

```bash
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT='587'
MAIL_USERNAME='username@domaine.me'
MAIL_PASSWORD='**********************'
SQLALCHEMY_DATABASE_URI='mysql://username:password@host:port/dbname'
```

#### Run the application

run the application to ensure that everything is working as expected.

```bash
flask run
```


#### Install NGINX

Install nginx.

```bash
sudo apt-get update
sudo apt-get install nginx
```
#### Configure Nginx

create new configuration to configure Nginx as a reverse proxy for your Flask app.

```bash
sudo nano /etc/nginx/sites-enabled/<directory-name-of-flask-app>
```

The contents of the confiugration file should be as follows:

```bash
server {
    listen 80;
    server_name <public-server-ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Unlink the default config file and reload nginx to use the newly created config file.

```bash
sudo unlink /etc/nginx/sites-enabled/default
sudo nginx -s reload
```

#### Installing and Using Gunicorn

```bash
sudo apt-get install gunicorn
```

Run the flask web app with gunicorn. The name of your flask instance must be app

```bash
gunicorn -w 3 flask_app:app
```

Now navigate to your servers public ip from a web browser! :)

## That's it!

Now , let's go to the home page

![Home](/uploads/80bda3d3eef74ad7aa67c43efa7b8d6b/Home.jpeg)

By, typing to any of the sections of the navbar you can navigate to any element in the website, For example let's
go ahead and clickon OUR COURSES

![Courses](/uploads/a6ec908a504472cd24bdd7e0214ca2fd/Courses.PNG)

contact section , for sending a review to SINGRA TEAM

![contatctUS](/uploads/96824d527487a6541f160f3382a5519f/contatctUS.jpeg)

After clicking to send message button , a verification email message will be receiving

![gmail1](/uploads/ecf049db43ae6a0e4246007007910190/gmail1.jpeg)

another way to navigate the page is by using the footer

![footer](/uploads/de7f500f00283c10857408ec2f7c9ce7/footer.jpeg)

About-us section will give a good idea about our services

![aboutUS](/uploads/86e68805516c8eb181022678c97c3e6b/aboutUS.jpeg)

now let's try to access to the dashboard to do some transactions

![CLickDashboard](/uploads/9f2545168517aae0d1e3924175fa8689/CLickDashboard.jpeg)

Oops ! you need to enter your informations first , LOGIN section opened automaticaly

this is the most important part here,

![SIghUP](/uploads/702d53f95f1351c630cfbc3a6a3cc542/SIghUP.jpeg)

then, you need to create an account first, Sign in section will open automaticaly

![LogINincorrect](/uploads/2f80731717cc5d826b967b18f5174bf3/LogINincorrect.jpeg)


a verification email message will be sending,

![gmail2](/uploads/b0793448741e99fb504f75f464970e50/gmail2.jpeg)

click the link to activate account

![emailActivation](/uploads/9322aca5d79f52ae0b419646b75657f0/emailActivation.jpeg)

Back again to login page, enter your own email and password ,and that's it , you're admin

![dashboard](/uploads/d12e73a23cea23fabb2eb164d2b60c43/dashboard.jpeg)

Dashboard is another page that help you to manage your profile,courses,bookmars and Calendar...
here, you can change and add more infomations to complete your profile

![Profile](/uploads/fa1d92f443a894619a5b2391617b0a5c/Profile.jpeg)
click save button , to update your changes

you can also change your password

![changePass](/uploads/225a386972aeca2851644f7b256e932a/changePass.jpeg)

Now, let's try to log out

![LogOUT](/uploads/232a87d03301fcde136f45b30c329483/LogOUT.jpeg)

let's try to click on forget password

if you enter a abad input , it will return an error as the following

![renameSearch](/uploads/1ad6bde960859f64b5141e3bd7653aea/renameSearch.jpeg)

now , let's continue

## Contributing

[Yahya Lafdi](https://github.com/YahyaLafdi)
[Nour-eddine Lachgar](https://github.com/noureddine409)
[Hamid Idifi](https://github.com/HamidIdifi)

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
