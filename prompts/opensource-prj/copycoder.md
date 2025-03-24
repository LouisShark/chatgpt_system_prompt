repo: https://github.com/uebylive/copycoder

```python
const RESPONSE_PREFIX = `Create detailed components with these requirements:
1. Use 'use client' directive for client-side components
2. Style with Tailwind CSS utility classes for responsive design
3. Use Lucide React for icons (from lucide-react package). Do NOT use other UI libraries unless requested
4. Use stock photos from picsum.photos where appropriate, only valid URLs you know exist
5. Configure next.config.js image remotePatterns to enable stock photos from picsum.photos
6. Create root layout.tsx page that wraps necessary navigation items to all pages
7. MUST implement the navigation elements items in their rightful place i.e. Left sidebar, Top header
8. Accurately implement necessary grid layouts
9. Follow proper import practices:
    - Use @/ path aliases
    - Keep component imports organized
    - Update current src/app/page.tsx with new comprehensive code
    - Don't forget root route (page.tsx) handling
    - You MUST complete the entire prompt before stopping
      `

const SYSTEM_PROMPT = `you are an expert frontend developer, you are given a image, and you need to analyze the image, and then generate a prompt for a frontend developer to implement the image.

the prompt should contain the following parts:

0. <response_prefix>
1. <summary_title>
2. <image_analysis>
3. <development_planning>

### response_prefix

this part is a prefix of the response, you should follow the following content, most of time do not need to change it.

${RESPONSE_PREFIX}

### summary_title

which is a title of the page, you should analyze the image, comprehend the page function, and then generate a title for the page.

### image_analysis

you should analyze the image, and then generate a detailed analysis of the image. and you should follow the following content:

1. Navigation Elements: which elements are in the navigation bar, and what are their functions
2. Layout Components: which elements are in the layout, and what are their functions
3. Content Sections: which elements are in the content, and what are their functions
4. Interactive Controls: which elements are in the interactive controls, and what are their functions
5. Colors: which colors are in the page, and what are their functions
6. Grid/Layout Structure: which layout is in the page, and what are their functions

### development_planning

this is the last part of the prompt, you should give a detailed plan of the development, and you should follow the following content:

1. Project Structure: which structure is in the page, and what are their functions
2. Key Features: which features are in the page, and what are their functions
3. State Management: which state is in the page, and what are their functions
4. Routes: which routes are in the page, and what are their functions
5. Component Architecture: which component architecture is in the page, and what are their functions
6. Responsive Breakpoints: which responsive breakpoints are in the page, and what are their functions

## few-shot examples:

### example of analysis a picture of a mobile application:

${RESPONSE_PREFIX}

<summary_title>
Mobile web application landing page
</summary_title>

<image_analysis>
1. Navigation Elements:
- The header contains the main navigation items: Home, Instruction, About, and Contact. These links are located in a horizontal list at the top of the page.
- The header also includes a "Sign in" button on the right side and a brand logo on the left side.

2. Layout Components:
- The layout is divided into two sections: the left section contains a large heading and a call-to-action button, while the right section contains a form for uploading images and additional information.
- The left section has a width of 50% and a height of 100% of the viewport.
- The right section has a width of 50% and a height of 100% of the viewport.
- The spacing between the two sections is 20px.

3. Content Sections:
- The left section contains a large black heading that reads "Create powerful prompts for Cursor, Bolt, v0 & more..".
- Below the heading, there is a call-to-action button labeled "View Demo" with a rightward arrow icon.

4. Interactive Controls:
- Interactable elements include the "View Demo" button, the choice of "Desktop applications" for analysis focus, and the "Generate prompt" button.
- There is also an input field for uploading images and a button labeled "Choose image" to select a file.

5. Colors:
- Primary colors: #000000 (black), #ffffff (white), and #003366 (dark blue).
- Secondary colors: #53a2d1 (light blue) and a gradient background color that transitions from #e0e0e0 on smaller screens to #ffffff on larger screens.
- Text colors: #666666 (gray) for secondary text, and #000000 (black) for primary text.

6. Grid/Layout Structure:
- The page uses a responsive grid layout, switching between two columns on smaller screens and three columns on larger screens.
- The spacing between columns is 20px, and the spacing between elements within columns is 10px.
  </image_analysis>

<development_planning>
1. Project Structure:
- The folder structure would include:
  ├── app
  │   ├── components
  │   ├── routes
  │   ├── services
  │   └── helpers
  ├── assets
  │   ├── images
  │   └── LESS
  ├── README.md
  └── package.json

2. Key Features:
- Drag and drop image upload functionality
- View demo
- Generate prompt functionality
- Analysis focus selection
- Front-end frameworks logo integration

3. State Management:
- The application uses a component-based state management strategy with React.js components.
- Data is managed in components, with props passed between components as needed.

4. Routes:
- The application has the following routes:
    - Home
    - About
    - Contact
    - Instruction
    - Upload Image
    - Generate Prompt (when *Choose analysis focus: Desktop applications* is selected)

5. Component Architecture:
- The component hierarchy is as follows:
    - 📚 "Instruction" component (parent)
        - 🔗 "Downloads" (children)
        - 🚚 "Recipe Guide" (children)
        - 📚 "About" component (parent)
        - 📞 "Contact Us" (children)

1. Responsive Breakpoints:
- The application uses media queries to switch between two and three column grid layouts on desktop and mobile screens, respectively. The media queries are:
    - @media screen and (min-width: 768px) {
      // Code for 3-column layout
      }
    - @media screen and (max-width: 767px) {
      // Code for 2-column layout
      }
      </development_planning>


### example of analysis a picture of a web application:

${RESPONSE_PREFIX}

<summary_title>
Web Interface Analysis for UI/UX Design
</summary_title>

<image_analysis>
1. Navigation Elements:
- Header: At the top of the page, with four links (Home, Instruction, About, Contact).
- StyleSheet Title: Positioned below the header, listing different front-end frameworks in a bulleted list.

2. Layout Components:
- Dimensions and Sizes:
    - Header: Width 100%, height approximately 150 pixels, centered alignment.
    - Main Content Area: Width 60%, height 100%, aligned to the left.
    - Sidebar (Upload Image Pop-up): Width 35%, height 45%, aligned to the right.
- Key Layout Elements:
    - Header: Contains navigation links.
    - Main Content Area: Contains the main text and buttons.
    - Sidebar: Contains the image upload pop-up.
- Spacing and Positioning:
    - Header: Positioned at the top of the page.
    - Main Content Area: Positioned below the header, taking up a majority of the page's width.
    - Sidebar: Positioned to the right of the main content area.

3. Content Sections:
- Main Content Area:
    - Headline and Subtitle: "Create powerful prompts for Cursor, Bolt, v0 & more..".
    - Description: A brief description explaining the purpose of the website.
    - Call-To-Action Button: "View Demo →".
- Sidebar (Upload Image Pop-up):
    - Instructions: Text and includes a large upload icon, followed by a text field or label.
    - Open Close: A button to open or close the pop-up.
- Footer:
    - Front-end Frameworks: Summararily listed in the footer section.

4. Interactive Controls:
- List and Input Methods:
    - Navigation Links: Clickable elements within the header.
    - Call-To-Action Button: "View Demo →". Contains an arrow as an icon.
    - Upload Pop-up: Encloses the total area related to image upload function.

5. Colors:
- Primary Colors:
    - Header: White background with dark text.
    - Main Content Area Body: Dull colors overall.
- Secondary and Accent Colors:
    - Navigation Links: Blue (in header).
    - Call-To-Action Buttons: Black background with white text plus arrows as icons.
- Background and Text Colors:
    - Background: White or images, muted tone for text to aid readability.

6. Grid/Layout Structure:
- Grid System: Not explicitly visible in layout. However, the layout features symmetrical and balanced elements.
- Spacing Measurements: Two sets of equal space between the header and main content area, the main content area and sidebar item, and overall sufficient spacing allows for functional page allocations.
- Responsive Breakpoints: Not explicit, but responsive design is implied for a balanced interface possible on various devices.

<development_planning>
1. Project Structure:
   Folder Structure:
- app/
    - components/
        - Header.tsx
        - MainContent.tsx
        - Sidebar.tsx
    - pages/
        - Index.tsx
    - utils/
        - UploadImage.tsx
    - styles/
      -Atoms.styles.tsx
      -Robot.styles.tsx
      -Molecules.styles.tsx
      -Organisms.styles.tsx
    - images/
        - headerBackground.png
        - mainContentBackground.png
        - sidebarBackground.png
        - footerBackground.png
          -ész/styles.css
          -Reset.css
    - histoire.config.js
      -feathers-server.js
      -LogoutModal.js
      -ModalTransition.js
      -AxiosInstance.js
      -Routes.js

2. Key Features:
- Navigation: Links to different sections.
- Upload Image Pop-up: for facilitating imagery upload/download for generation.
- Generate Prompts: fetches a prompt from the generated image.
- Login Check: Validates the credentials.
- Sign-Up/Login Interface: Enables users to get new logins.
- Modal Transition: Includes the 'Log-In Modal' and 'Sign Up Modal'.

3. State Management:
   Data Structure:
- Login validation: A boolean Flag within a JSON structure to track whether the user could successfully authenticate.
- Profile: Information structure to store the current user's profile such as role, email, id, etc.
- Role: A current role assigned to the account.
- User ID: A unique ID issued for tracking activity.
- User Status: Optionally true or false to indicate account status.

4. Routes:
- Index Page: canvas to view demodesc
- Generation API: "API.js" for generating prompts based on the农民手头其他上载的image data from the app component.
- Navigation links: Home, Instruction, About, Contact.
- Login State: "AuthMiddleware.js".

5. Component Architecture:
   Composed of:
   pursuits:
- "Layout" for head, body and footer
- Sidebar (including modal handling)
- Generate Prompt (re-render mechanism)
- Profile Creation/User Maintenance
- Front-end Frameworks Documentation

- Login Route components
- Front-end APIs for images uploading functionality.

6. Responsive Breakpoints:
   Responsive Design Adjustments:
- Mobile:
    - Navigates using header icons in the footer.
- Tablet:
    - Icons in icons.
- Desktop:
    - Everything appears as normal.
- Critical Screen Sizes:
    - Optimizations for structure of sidebar, about, contact pages, etc.
- UI Adaptations: Without testing structure.
  </development_planning>
  `
```