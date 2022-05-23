### Table of contents:

[Purpose](#purpose)

[User Stories](#user-stories) 

[Design and UX](#design-and-ux) 
* [Wireframes](#wireframes)
* [Database model](#database-model)

[Features](#features)

[Future Implementations](#future-implementations)

[Technologies](#technologies)

[Testing ](#testing)
* [Code Validation](#code-validation)
* [Browser Compatibility](#browser-compatibility)
* [Performance Testing](#performance-testing)
* [Manual Testing](#manual-testing)
* [Automated Testing](#automated-testing)
* [User Stories Testing](#user-stories-testing)

[Debugging and known bugs](#debugging-and-known-bugs)

[Deployment](#deployment)

[Credits](#credits)

[Resources](#resources)

[Acknowledgements](#acknowledgements)

### Purpose



Live link:
[]()

Screenshot:
![]()

### User Stories

**Theme**

A website to assist individuals in coming out as LGBTQ+.

**Epic**

The website allows the user (creator) the ability to create a private page which can securely be sent to individuals (viewer). Only specified viewers can see the page, and the creator controls the content of the page. Content may include: personal photos/videos/text and educational/explanatory resources for viewers who may need them.

**User stories**

* As a creator, I can securely sign into the website so that my information is kept private.

* As a creator, I can create a private page with a personal photo, video or text so that I can personalise my coming-out.

* As a creator, I can add resources to my page so that I can educate the viewer if needed.

* As a creator, I can edit my page so that I can make changes if they are needed.

* As a creator, I can securely share a page with specified viewers so that I can come out to them without being in the same physical space.

* As a creator, I can privately share a page so that I can come out without my private information being freely available on the web to anyone other than the specified viewer.

* As a viewer/creator, I can sign in intuitively so that I can use the website easily.

* As a viewer/creator, I can navigate the website easily and intuitively.

* As a viewer, I can view a creator’s page so that I can learn about the creator.

* As a viewer, I can follow resource links so that I can learn more about the creator’s sexuality/gender identity and find out how to be supportive.

* As a site owner, I can provide access to educational/explanatory resources that could be useful to creators and viewers so that the user does not have to do their own research if they don’t want to.

* As a site owner, I can provide a secure and private platform so that creators can come out on their own terms.

### Design and UX

### Wireframes

### Database model


### Features

Landing page - website title and 'about' text to clearly and briefly explain the purpose of the site.

Landing page - viewer and creator login links.

Creator login page - email and password required.

Viewer login page - email, password and specific creator code required.

Navigation bar - logo, login/logout, profile and resources.

Creator profile - personal page/s with associated code/s. Link to create new page.

Viewer profile - page/s they have been given permission to view.

Resources page - card view of links to external resources.

Create new page - new form with accessible fields including title/author, photo/video/s, any extra text, any link/s, link to resources page, title for link, url for link. All fields are optional. Submit button and once submitted the page will have an edit button, both will have user feedback.

### Future Implementations

check if this section should go here
viewer email - more than one allowed per viewer
chat - separate for viewers and creators
ability for creators to suggest resources
video upload

### Technologies

Languages used:

Python 3

HTML5

CSS

Javascript

Frameworks, Libraries and Programs Used:
Django/allauth/summernote
Bootstrap
Cloudinary
SQLite (default Django database)
EmailJS

GitHub - for hosting the site

Heroku - for the deployment of the site

Gitpod - for editing the files

### Testing 

### Code Validation

[Python validator](http://pep8online.com/) - 

[Javascript validator](https://jshint.com/) - 

[HTML validator](https://validator.w3.org/) - 

[CSS validator](https://jigsaw.w3.org/css-validator/) - 

### Browser Compatibility

Browser Compatibility checks were run using [BrowserStack](https://www.browserstack.com/) and my computer. The results are:

Firefox - &#9745;

Chrome - &#9745;

Opera - &#9745;

Safari - &#9745;

Microsoft Edge - &#9745;

### Performance Testing

Performance testing was conducted using [Lighthouse](https://developers.google.com/web/tools/lighthouse#devtools). The results are:

![Lighthouse results]()

### Manual Testing



I conducted manual testing and recorded the results as follows:

![Manual testing](assets/readme-files/images/manual-testing-rhubarb-witch.jpg)

### Automated Testing

### User Stories Testing

### Debugging and known bugs

### Deployment

### Publishing

The project was deployed using Heroku. The process is as follows:

Once you have signed up to Heroku, on the top right of the dashboard there is a button labelled 'New'. This will open a dropdown; please select 'Create new app'. On the next page you can choose your region and a name for the project. Then click 'Create app'.

On the next page there is a menu along the top. Navigate to 'Settings', where you will find the config vars. Scroll down to the section named 'Config vars' and click on the button labelled 'Reveal config vars'.

CONFIG VAR INFO HERE AND CORRESPONDING GITPOD CHANGES NEEDED

If you scroll back to the top of the page you will find the 'Deploy' tab, which has multiple options for deployment. I used Github for this project. When you click on the Github button a bar will come up for you to search for the repo you wish to connect to.

Once you have connected, you have the option to deploy automatically (the app will update every time you push) or manually (update only when you choose). I chose automatic but you can do what suits you.

After the first push/update, your app will be ready to go!

As of the publishing of this site (May 2022) Heroku is not currently allowing automatic deployment from Github. In order to deploy manually, the steps are (courtesy of Jim Morel from the Code Institute):

1. Open the terminal.
If you are using MFA/2FA: please scroll down to see the additional steps required.
Otherwise:
2. Enter 'heroku login -i' in the terminal and enter your own login details. 
3. Enter 'heroku apps' in the terminal.
4. Set the Heroku remote. Enter the following command in the terminal: 'heroku git:remote -a out-proud'
5. Enter the following command in the terminal: 'git add . && git commit -m "Deploy to Heroku via CLI" '
6. Push to both GitHub and Heroku with the two followig commands:
Enter the following command in the terminal: 'git push origin main'
Enter the following command in the terminal: 'git push heroku main'

*Do you have MFA/2FA enabled?* If so, please:
Click on Account Settings (under the avatar menu) on the Heroku Dashboard.
Scroll down to the API Key section and click Reveal. Copy the key.
In the Gitpod workspace, enter the following command in the terminal: 'heroku_config' , and enter your API key that you copied when prompted.
Continue from step 3 above. If you get prompted to log in at any point enter your username and the API key you copied.

### Forking and Cloning
 
To save a copy of the code and work on it yourself, here are the steps for forking and cloning using Github:

In the repository, click the 'Fork' button, which is on the top right-hand side, next to 'Star'.

Github will automatically create a new repo, which is forked from the original. If you would like to clone it you have two options:

Within the repository, click the 'Code' dropdown, which is located next to 'Add File' on the right (underneath the Settings tab); there is an option to download all files and save a copy locally.

In the same 'Code' dropdown, you can opt to open the code with GitHub Desktop and work from there.

### Resources

Mention all official documentation referenced in code here eg django, cloudinary, bootstrap, look through bookmarks. DjangoGirls.

Guidance with updating and deleting Page instances from [GeeksforGeeks](https://www.geeksforgeeks.org/django-crud-create-retrieve-update-delete-function-based-views/).

Photo editing from [Pixlr](https://pixlr.com/).

Favicon generated from [Favicon.io](https://favicon.io/favicon-converter/)

### Credits



Placeholder image from artist [Bee](https://beebeedibapbeediboop.tumblr.com/); used with permission from the artist.

### Acknowledgements


