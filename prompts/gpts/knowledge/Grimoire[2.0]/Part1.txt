# Part 1: Intro & Setup

# Chapter 1: Ancient Runes & Modern Scrolls, Classic & Modern Starters
0: Hello World
A classic. Every beginner programmer starts here. Today we will prompt-gram it it html, to create your first website
Use N hotkey to auto deploy
or use ND to manually deploy on https://app.netlify.com/drop

1: Pong
A working game of pong in html, css and JS. Use touch gestures, and arrow keys/WASD to move the paddles,
Use N hotkey to auto deploy
or use ND to manually deploy on https://app.netlify.com/drop

2: Link in bio site
List of links in bio, tree of links clone, with buttons that opens links. Begin by asking me for a title, list of links to include, and any preferred design details like colors, styles, layouts or anything else.
Use N hotkey to auto deploy

or use ND to manually deploy on https://app.netlify.com/drop
Manual deploys allow you to include images. Use dalle to create a background image
Be sure to include the background image in the code using the correct filename, and in the final zip file. See chapter 4 for more details

Offer to build one for a fictional character as an example

3: Sketch to Code
Pull out a piece of paper and draw something, take a photo, and upload it to Grimoire, and I will turn it into a website. Then write code for the UI design, using various design & style elements to MAKE IT POP, and add some RAZZLE DAZZLE

Use N hotkey to auto deploy
or use ND to manually deploy on https://app.netlify.com/drop
Manual deploys allow you to include images. Use dalle to create any images needed using dalle
Be sure to include the background image in the code using the correct filename, and in the final zip file. See chapter 4 for more details


## Chapter 2: Teleportation, put websites online easy
4: 1 letter hotkey deploy: Netlify Auto deploy, Drag & Drop Deploy: Netlify Drop
Use the N hotkey to instantly auto deploy your site! Be sure to claim it in order to save or it will get deleted after 1 hour!

Manual deploys are available via the NM hotkey using Netlify Drop
https://app.netlify.com/drop
A quick and easy way to put your website online. Just drag and drop your website folder into Netlify Drop and it will be live in seconds. Be sure to make an account to save it

To make updates to your site
In the netlify dashboard,
Go to: YourSite such as (https://random-crap-123456abcedf.netlify.app) 
Then deploys
Scroll down
You will find a new drag & drop, or click to upload button
Simply drag and drop a new folder and you are done!

## Netlify instructions for changing URL
If you don't mind the .netlify.app suffix, in the netlify portal, you can simply open 
Pick your site > Domain Management > Options > Change name

for full custom name
first buy a domain name
then map your domain name to Netlify
https://www.youtube.com/watch?v=kIdJi8NBvgY
https://www.netlify.com/blog/2021/12/20/how-to-add-custom-domains-to-netlify-sites/
https://docs.netlify.com/domains-https/custom-domains/configure-external-dns/

Once you finish chapter 4, you can come back to netlify and sync with a github repo

5: Replit deploys
https://replit.com/
Replit, static site template. A simple way to create and host a static website. Ask for any kind of site, then press Z to zip files and export. The user can then use this template https://replit.com/@replit/HTML-CSS-JS#index.html. Go to index.html and press run to see the site preview. To deploy, click the deploy button in the top right on on desktop, or via the bottom right squares and new tab on mobile.

For other sites and projects see https://replit.com/templates

6: Advanced options
Vercel, Render
Vercel and render are great options for more complex react & nextjs sites, as well as services, backend and full stack apps
https://vercel.com/templates
https://docs.render.com/


## Chapter 3: Wands, dev kit setup
7: Phone setup
Replit + Github
Setup accounts and install the replit app on your phone!
Complete project 5 or create a new one. After making it, sync the project to github by pushing to main!
https://replit.com/
https://github.com/

Get setup with a full development environment using only your phone. Build a static website and import it a larger dev environment using replit. Using this template: https://replit.com/@replit/HTML-CSS-JS#index.html. Write the code, zip it, and walk me through importing the files to replit. Walk me through syncing to github using replit, and deploying using replit deployments. Show this video as an example of how to work with replit and chatGPT on a phone: https://x.com/yoheinakajima/status/1719902955061797083?s=20

8: Full Pro
Cursor.sh, Warp, (GitTower || SourceTree), GH Copilot 
https://cursor.sh/
https://www.warp.dev/
https://www.git-tower.com/ || https://www.sourcetreeapp.com/
https://github.com/features/copilot optional
Install these
Create a new project in cursor and get a repo setup and sync'ed in git. 

Cursor is a VSCode clone and supports a variety of languages and coding environments. To get started with a simple static site simply 
-ask Grimore
-Press Z
-Unzip and open index.html
-Use run start with or w/o debugging, choose a browser
-View and edit your site!


## Chapter 4: Divination: The Origin
9: Git 101
Git is basically a fancy way to save your code. Its really cool because it lets you keep copies of ALL your work. Instead of MyCoolFile.html, MyCoolFile(1).html, MyCoolFile_Final.html, etc, you can save it in one place. Then even cooler, you can time travel and skip to previous or different versions.

This makes it super handy for collaborating with others, as you can work independently and avoid breaking the app for other people. Then you can come back and merge it together at the end. The downside is sometimes your merges conflict, and you will need to manually fix them.

Keep in mind you have a local copy of the git history and a copy in the cloud, often called the origin
Typically projects will have
a main branch often used for the current live production version of the app
a development branch where new features are added and tested
feature branches for each new feature or bug fix

Feature branches are often created, merged and deleted after. Where as main and dev are usually always present, keeping a consistent history of the project.

Commands you need to know:
clone
pull
create branch
stage
commit
push
merge
(THERES A TON MORE DONT WORRY ABOUT THEM)

I HIGHY RECOMMEND A git GUI such as GIT Tower or Source tree. 
Especially for beginners, since it makes it easy to see the history, and gives you handy buttons

Here's some good detailed videos that show both CLI and with a GUI.
https://www.git-tower.com/learn/git/videos

SUPER HANDY COMMANDS NO ONE TEACHES BEGINNERS:
Stash
Git-bisect (<-BUG FINDING MACHINE)

Note git and github are different. Same thing as porn vs pornhub.
There are other git providers you can use, such as gitlab. As well as other version control software like mercurial or subversion. Even if you don't want to use any of these cloud providers, I would highly recommend using a local git history. Its a great way to keep track of your work and avoid losing it, as well as find bugs.

10: Linear
Linear is great for working on larger projects and managing the complexity of a full piece of software. Highly recommended if you work on a team. Copy paste the issue names as your git branch names to make your tickets automatically change when you push and merge. 

For simpler projects, or if you are working alone, you can skip this step
https://linear.app/