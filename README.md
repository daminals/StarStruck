![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue)  ![github repo badge: Built%20With](https://img.shields.io/badge/Built%20With-Visual%20Studio%20Code-181717?color=blue)  ![github repo badge: Using](https://img.shields.io/badge/Using-Coinbase-181717?color=blue)  ![github repo badge: Powered%20By](https://img.shields.io/badge/Powered%20By-Astrology-181717?color=purple)
# StarStruck🚀

> If StarStruck loses money it's because its a Scorpio ♏️

A Crypto Wallet with an Astrology-Based Investment Algorithm 

<div align="center">
<img src='https://github.com/daminals/StarStruck/blob/master/static/graph/Portfolio.png'>
</div>

<details>
<summary>Flask Component</summary>

 **Layout of the Application** <br/>

<img src="https://github.com/daminals/StarStruck/blob/master/static/markdownResources/layout.png" /> <br/>
The frontend displays user graphs, as well as access to the various coins owned by the user in non-zero wallets. The user has access to their total portfolio, and data on all the coins they own. All web pages are built via the same template, and fed in backend information through Flask.

<br> **JQuery Integration** <br/>
JQuery seamlessly communicates with the Flask backend to effortlessly update the information server side on the firebase database, as well as client side via updating the user graph without reload

<br> **Easily Expandable Routes**  <br/>
The application is structured such that it will update automatically for every coin the user buys. This is because none of the data that is liable to change is static or enumerated, and so the web pages and links are built through Flask's templating system.
<br/>
<br/>
</details>

<details>
<summary>Coinbase API and Custom Wrapper</summary>

**Buying and Selling** <br/>
boring explanation boring explanation boring explanation

<br/>  **Custom Wrapper** <br/>
As many parts of Coinbase's python3 API wrapper did not work as intended, a custom wrapper built to access this data was built. It wraps GET and POST requests within the needed functionality.
<br/>
<br/>
</details>

<details>
<summary> Portfolio </summary>

**Graphing from Firebase** <br/>
Reading and setting data to and from Firebase Real Time Database and using said data in conjunction with Matplotlib to show current graphs of the Portfolio value over time and the individuals coin values over time
<br/>
<br/>

</details>

<details>
<summary> Astrology-based Algorithm </summary>

**Work in Progress** <br/>

<br/></details>
