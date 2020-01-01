Analyzing the contents of (almost) every National Geographic magazine since its inception in 1888. 

## Exploration

Before I started with any specific question in mind, I set out to explore Nat Geo's online archive with an open mind. I didn't know what kind of data might be behind the website or if there would be any at all that's visible to the public - only that I wanted to find something interesting.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoCover.png" width="34%" align="right">

The first step I take nowadays is always checking Google Chrome's network page for any JSON files. Fortunately, Nat Geo keeps both an archive of every issue's metadata and additional data on the contents of each individual issue. Within each issue, there is information relating to an article's title, abstract, and page number. This even extends to tons and tons of photos, department notices, and editors notes.

There is also a folio breakdown that lists the order of pages within each issue - something that may be interesting to look at down the road. How did Nat Geo's page layout with respect to ad space change over time? Or something along those lines.

Unfortunately, Nat Geo is pretty spotty with their data management. As of December 2019, there have been 1,522 issues made and 50 of them (~3.3%) lack any JSON data to tell what is inside. Another 42 issues (~2.8%) have fewer than 5 tagged articles, photos, or other pages. The magazine issues with missing data are oddly clustered, with 45 of 50 falling from 2010-2014, 2 in 1992-1993, and the remaining 3 from 1893-1895. On the whole though, most issues have 150 or so well-defined tags listing the exact details of each article or photo. 

The breakdown of metadata (out of the 1,472 with JSON) is as follows.

<table>
<thead><tr"><th></th><th>All</th><th>Articles</th><th>Photos</th><th>Other</th></tr></thead><tbody>
 <tr><td>Max</td><td>996</td><td>23</td><td>982</td><td>24</td></tr>
 <tr><td>75th Percentile</td><td>223</td><td>7</td><td>212</td><td>3</td></tr>
 <tr><td>Median</td><td>167</td><td>6</td><td>158</td><td>1</td></tr>
 <tr><td>25th Percentile</td><td>61</td><td>4</td><td>55</td><td>0</td></tr>
 <tr><td>>= 1 Issues</td><td>1,472</td><td>1,459</td><td>1,365</td><td>846</td></tr>
 <tr><td>Total</td><td>225,828</td><td>8,407</td><td>213,049</td><td>4,372</td></tr>
 <tr><td>Avg</td><td>153.4</td><td>5.7</td><td>144.7</td><td>3.0</td></tr>
  </tbody></table>


So the bulk of Nat Geo's metadata is really in the photos. However, the photo titles are the only information immediately available and they are much shorter in length than article titles and abstracts (an average of 29 characters vs. 203). For the time being, I think it'd be wise to solely focus on the 8,407 tagged articles spanning the last century.

Example of photo title:

`Babasaki Gate, Tokyo, Japan`

Example of article title and abstract:

`Ascension Island, an Engineering Victory : Located halfway between South America and Africa, the tiny, bird-covered volcanic island of Ascension is a vital military refueling station with an airfield.`

## Asking Questions

Before digging into the text just yet, how about looking at simply the magazine itself over time? National Geographic <a href="https://www.nationalgeographic.com/news/2016/09/geographic-magazine-natgeo-first-hubbard-greely-1888/">began as more of a scientific journal</a> than a modern-day magazine, containing lengthy written passages on American surveying and geography. The first "photo" (a map of North America) appeared two issues later, and it wasn't until 1959 that a photo even appeared on the cover. Now Nat Geo is <a href="https://www.npr.org/sections/pictureshow/2013/10/01/227871549/national-geographic-celebrates-125-years-of-photography">synonymous with photographic achievement</a>.

Another clear difference between the original magazine and today's is its length. Up until the year 1900, Nat Geo averaged just under 58 pages per issue. This was followed by a steep increase in length through 1925, gaining an average of about 6 pages a year, which coincided with a <a href="https://www.wired.com/2010/01/0127national-geographic-society-founded/">change in editorial preferences</a> geared towards making the magazine more accessible and photo-heavy. And that's been right about where the magazine has settled in the century that has followed, hovering right around 165-180 pages.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoPages.png" width="66%" align="right">

Now returning to the article data that we've scraped, I see a few different avenues of research ahead. We have three pieces of data: the title and abstract of almost every article Nat Geo has ever released in print, when it was released, and what page the article was on. Let's ignore the page numbers for now and just focus on what questions can be drawn from text and dates. Since Nat Geo has predominantly been a global publication, we can think of most articles as being associated with at least one specific country. Whether it's an analysis of Rwanda's future or a dive into the Brazil-French Guiana border situation, it seems that one identifiable tag could be a country's name.

To test this theory, I automatically paired all applicable countries to every Nat Geo article's text (a combined title and abstract field) and wound up with a surprising number of matches. In total, 4,883 country tags were created pertaining to 3,890 unique articles, an average of ~1.3 countries per article. A few articles even had 5 countries mixed in, like <a href="https://archive.nationalgeographic.com/national-geographic/1966-dec/flipbook/Ad23/">this Dec. 1966 essay</a>:
`Abraham, the Friend of God : Following in the footsteps of the Old Testament patriarch who conceived the idea of one almighty God, the author pursues legend that is history from Iraq to Jordan, Syria, Turkey, Egypt, and Jerusalem.`

With this in mind, let's see if we can answer any of these questions:

**Has National Geographic's coverage of each continent changed over time?**

**At what frequency does National Geographic cover each country?**

**Does National Geographic cover countries proportionately to how populated they are? If not, what's driving coverage?**

## Continental Drift

Datahub.io provides a handy <a href="https://datahub.io/JohnSnowLabs/country-and-continent-codes-list">file</a> that, along with listing every modern-day country, also provides their continents. Now, a few disclaimers about how countries have been tagged and how that may or may not affect the result to follow.

1. Countries with variations in spelling had both versions added then re-combined after tagging (e.g., `Côte d'Ivoire` & `Ivory Coast`)
2. Some countries are admittedly impossible to differentiate via automated text search (e.g., `Democratic Republic of the Congo` & `Republic of the Congo`). In these cases, all text with `Congo` was assigned just one country.
3. Nat Geo has been around a while and a lot has changed since 1888. Burma became Myanmar, Korea split into North and South, Yugoslavia was created then dissolved, a large majority of Africa was under colonial rule, etc. The world was <a href="https://en.wikipedia.org/wiki/List_of_countries_by_population_in_1900">very different back then</a> and it's harder still to trace every country's names over the past 131 years. That's why I've only used modern-day countries in this search, which could drastically affect how often certain countries appear in the results. I think this is likely the largest challenge 
4. A few countries have naming issues that required manual editing. Five were simple liking removing references to `Dominica` when the text actually said `Dominican Republic` (e.g. `Nigeria`, `Papua New Guinea`) while others meant surfing through every tagged reference to `India` to make sure Nat Geo wasn't referencing Native Americans (e.g. `Georgia`, `Chad`).
5. Several countries are listed as being members of two continents (e.g. `Armenia`, `Turkey`), so for this continental breakdown both instances were kept. When talking about the countries themselves later on, only one instance is kept.

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoContinents.png" width="100%">

After plotting every continent's reference totals in Tableau, we get something like this. Keep in mind, the US has been removed from this dataset because there are just so many references to America that it's difficult to compare North America against any other continent.

It seems that, on the whole, the rate at which Nat Geo writes about various continents has stayed somewhat consistent. Fewer articles have been written about Europe since the mid-20th century, and I would speculate much of the interest from 1910-1950 was drawn from the World Wars. In Europe's place, more articles have been written about African and Asian countries lately and I'd expect that trend to continue as those countries grow in population. However, I think it's difficult to read too much into these figures without first looking at individual country coverage, which leads to the next question - what countries have been covered the most?

## Country Coverage

<img src="https://github.com/justinperline/natgeocoverage/blob/master/NatGeoCountries.png" width="100%">
