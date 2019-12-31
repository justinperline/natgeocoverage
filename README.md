Analyzing the contents of (almost) every National Geographic magazine since its inception in 1888. 

## Exploration

Before I started with any specific question in mind, I set out to explore Nat Geo's online archive with an open mind. I didn't know what kind of data might be behind the website or if there would be any at all that's visible to the public - only that I wanted to find something interesting.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoCover.png" width="30%" align="left">

The first step I take nowadays is always checking Google Chrome's network page for any JSON files. Fortunately, Nat Geo keeps both an archive of every issue's metadata and additional data on the contents of each individual issue. Within each issue, there is information relating to an article's title, abstract, and page number. This even extends to tons and tons of photos, department notices, and editors notes.

There is also a folio breakdown that lists the order of pages within each issue - something that may be interesting to look at down the road. How did Nat Geo's page layout with respect to ad space change over time? Or something along those lines.

Unfortunately, Nat Geo is pretty spotty with their data management. As of December 2019, there have been 1,522 issues made and 50 of them (~3.3%) lack the JSON data to tell what's inside. Another 42 issues (~2.8%) have fewer than 5 tagged articles, photos, or other pages. On the whole though, most issues have hundreds of well-defined tags listing exactly what each article is generally about or what each photo is of. Of issues with metadata, here is the breakdown of how well-tagged everything is:

<p align="center">
<table>
<thead><tr"><th></th><th>All</th><th>Articles</th><th>Photos</th><th>Other</th></tr></thead><tbody>
 <tr><td>Max</td><td>996</td><td>23</td><td>982</td><td>24</td></tr>
 <tr><td>75th Percentile</td><td>223</td><td>7</td><td>212</td><td>3</td></tr>
 <tr><td>Median</td><td>167</td><td>6</td><td>158</td><td>1</td></tr>
 <tr><td>25th Percentile</td><td>61</td><td>4</td><td>55</td><td>0</td></tr>
 <tr><td>Issues > 0</td><td>1,472</td><td>1,459</td><td>1,365</td><td>846</td></tr>
 <tr><td>Total</td><td>225,828</td><td>8,407</td><td>213,049</td><td>4,372</td></tr>
 <tr><td>Avg</td><td>153.4</td><td>5.7</td><td>144.7</td><td>3.0</td></tr>
  </tbody></table></p>
