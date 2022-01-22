<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
--> 

<!-- <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/OpenPIL/OpenPIL?color=brightfreen&logo=github"> -->
<!-- <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/OpenPIL/OpenPIL?color=brightgreen&logo=github"> -->
<!-- https://img.shields.io/badge/🏆%20Awards-University%20of%20Manchester%20Making%20A%20Difference%20Award-brightgreen?style=flat&logo=UniversityOfManchester?style=flat -->





<!-- PROJECT LOGO -->

<br>

<br />
<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/OpenPILReadME.png" alt="Logo" height="150" style="padding-top: 100px">
  </a>
    <br>
    <br>
  <h3 align="center">The non-profit open-source AI making medication information free and safe for the developing world.</h3>
    <br>
<!-- 
  <p align="center">
     -->
  </p>
</div>

<p align="center">
  <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
          <img src="https://img.shields.io/badge/organisation-Non--Profit-brightgreen?style=flat&logo=UniversityOfManchester?style=flat" /></a>
  <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/license/OpenPIL/OpenPIL?color=brightgreen" /></a>
    <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
          <img src="https://img.shields.io/badge/🏆%20awards-University%20of%20Manchester%20Making%20A%20Difference%20Award-brightgreen?style=flat&logo=UniversityOfManchester?style=flat" /></a>
      <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/languages/count/OpenPIL/OpenPIL?color=brightgreen?style=flat" /></a>
    <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
          <img src="https://img.shields.io/badge/pypi%20package-v2.0.1-brightgreen?style=flat" /></a>
    <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
          <img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-brightgreen?style=flat" /></a>
</p>

<br>
<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- TABLE OF CONTENTS -->
## Table of Contents

<!-- <details> -->
<!--   <summary>Table of Contents</summary> -->
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
         <ul>
             <li><a href="#what-we-do">What is OpenPIL AI?</a></li>
             <li><a href="#why">Why?</a></li>
             <li><a href="#how-does-it-work">How does it work?</a></li>
        </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#datasets">Datasets</a></li>
    <li><a href="#roadmap">Development</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
  
<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>
<!-- </details> -->

<!-- ABOUT THE PROJECT -->

## About The Project

### What We Do.
OpenPIL is a registered non-profit organisation that has built an artificial intelligence algorithm to extract essential drug information from public domain Summary of Product Characteristic Documentation. Through this, we aim to soon compile the largest and most up-to-date medication information database in existence, and then make it free for the world. The project has already won a highly competitive and prestigious award from the University of Manchester.

### Why?
This essential clinical information is currently highly-privatised, which restricts access and puts peoples lives at risk. This is particularly of concern for those in developing or war-torn countries, whose access to up-to-date medicinal information is limited, even though it doesn't have to be.

Use the `BLANK_README.md` to get started.

### How We Are Doing It?
The AI currently retrieves information on active-substances, formulations, active-excipients, and drug-drug interactions. Research is being carried out to continuously improve the AI's reliability and accuracy. We are aiming to soon expand the AI to handle information pertaining to a medication's indications, cautions, advisory instructions, side-effects, safety of use during pregnancy, and storage conditions. This pharmaceutical data will also be very valuable to healthcare startups, local pharmacies, open-source drug development projects and medicinal researchers.

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- GETTING STARTED -->
## Getting Started

These are the instructions to install the OpenPIL AI locally and get started with analysing those Summary of Product Characteristics Documents (.pdf).

### Installation
The OpenPIL AI is really easy install. Simple type the below command into your terminal.

```
pip install OpenPIL
```
<!-- <br> -->

_or_

```
pip3 install OpenPIL
```
<!-- <br> -->

_or_
```
python3 -m pip install OpenPIL
```
<!-- <br> -->

_If this doesn't work, make sure you have the dependencies, as can be seen below._

<p align="right">(<a href="#top">back to top</a>)</p>

### Dependencies

You will need the latest version of python if you are still running python2.
```
pip install --upgrade python
```

You will need the following modules (nltk, PyPDF2, pdftotext):

```
pip install nltk
```
```
pip install PyPDF2
```
```
pip install pdftotext
```

_or if you already have them_
```
pip install --upgrade nltk
```
```
pip install --upgrade PyPDF2
```
```
pip install --upgrade pdftotext
```

All other modules should come pre-installed with Python3, they as follows incase you are missing any:

```
pip install re
```
```
pip install string
```
```
pip install math
```
```
pip install ctypes
```
```
pip install sys
```
```
pip install platform
```
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
### Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

## Datasets

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>


<div align="center">
    <a href="https://github.com/OpenPIL/OpenPIL">
    <img src="/Assets/Seperator 20.59.10.png" alt="Logo" width="100%">
  </a>
</div>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
