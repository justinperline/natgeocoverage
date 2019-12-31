Analyzing the contents of (almost) every National Geographic magazine since its inception in 1888. 

## Exploration

Before I started with any specific question in mind, I set out to explore Nat Geo's online archive with an open mind. I didn't know what kind of data might be behind the website or if there would be any at all that's visible to the public - only that I wanted to find something interesting.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoCover.png" width="28%" align="left">

The first step I take nowadays is always checking Google Chrome's network page for any JSON files. Fortunately, Nat Geo keeps both an archive of every issue's metadata and additional data on the contents of each individual issue. Within each issue, there is information relating to an article's title, abstract, and page number. This even extends to tons and tons of photos, department notices, and editors notes.

There is also a folio breakdown that lists the order of pages within each issue - something that may be interesting to look at down the road. How did Nat Geo's page layout with respect to ad space change over time? Or something along those lines.

Unfortunately, Nat Geo is pretty spotty with their data management. As of December 2019, there have been 1,522 issues made and 50 of them (~3.3%) lack any JSON data to tell what is inside. Another 42 issues (~2.8%) have fewer than 5 tagged articles, photos, or other pages. The magazine issues with missing data are oddly clustered, with 45 of 50 falling from 2010-2014, 2 in 1992-1993, and the remaining 3 from 1893-1895. On the whole though, most issues have 150 or so well-defined tags listing the exact details of each article or photo. 

The breakdown of metadata (out of the 1,472 with JSON) is as follows.

<p align="center">
<table>
<thead><tr"><th></th><th>All</th><th>Articles</th><th>Photos</th><th>Other</th></tr></thead><tbody>
 <tr><td>Max</td><td>996</td><td>23</td><td>982</td><td>24</td></tr>
 <tr><td>75th Percentile</td><td>223</td><td>7</td><td>212</td><td>3</td></tr>
 <tr><td>Median</td><td>167</td><td>6</td><td>158</td><td>1</td></tr>
 <tr><td>25th Percentile</td><td>61</td><td>4</td><td>55</td><td>0</td></tr>
 <tr><td>>= 1 Issues</td><td>1,472</td><td>1,459</td><td>1,365</td><td>846</td></tr>
 <tr><td>Total</td><td>225,828</td><td>8,407</td><td>213,049</td><td>4,372</td></tr>
 <tr><td>Avg</td><td>153.4</td><td>5.7</td><td>144.7</td><td>3.0</td></tr>
  </tbody></table></p>

So the bulk of Nat Geo's metadata is really in the photos. However, the photo titles are the only information immediately available and they are much shorter in length than article titles and abstracts (an average of 29 characters vs. 203). For the time being, that meant I'd focus solely on the 8,407 tagged articles spanning the last century.

Example of photo title:

`Babasaki Gate, Tokyo, Japan`

Example of article title and abstract:

`Ascension Island, an Engineering Victory : Located halfway between South America and Africa, the tiny, bird-covered volcanic island of Ascension is a vital military refueling station with an airfield.`

## Asking Questions

Before digging into the text just yet, how about looking at simply the magazine itself over time? National Geographic <a href="https://www.nationalgeographic.com/news/2016/09/geographic-magazine-natgeo-first-hubbard-greely-1888/">began as more of a scientific journal</a> than a modern-day magazine, containing lengthy written passages on American surveying and geography. The first "photo" (a map of North America) appeared two issues later, and it wasn't until 1959 that a photo even appeared on the cover. Now Nat Geo is <a href="https://www.npr.org/sections/pictureshow/2013/10/01/227871549/national-geographic-celebrates-125-years-of-photography">synonymous with photographic achievement</a>.

Another clear difference between the original magazine and today's is its length. Up until the year 1900, Nat Geo averaged just under 58 pages per issue. This was followed by a steep increase in length through 1925, gaining an average of about 6 pages a year, which coincided with a <a href="https://www.wired.com/2010/01/0127national-geographic-society-founded/">change in editorial preferences</a> geared towards making the magazine more accessible and photo-heavy. And that's been right about where the magazine has settled in the century that has followed, hovering right around 165-180 pages.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoPages.png" width="48%" align="right">

We have three pieces of data at this point: the title and abstract of almost every article Nat Geo has ever released in print, when it was released, and what page the article was on. Let's ignore the page numbers for now and just focus on what questions can be drawn from text and dates.

Has National Geographic's coverage of each continent changed over time?

At what frequency does National Geographic cover each country?

Does National Geographic cover countries proportionately to how populated they are? If not, what's driving coverage?
