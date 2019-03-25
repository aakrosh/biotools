#!/usr/bin/env Rscript

# this is just a script for the steps detailed here: http://tuxette.nathalievilla.org/?p=1682

get_all_publications = function(authorid) {
  # initializing the publication list
  all_publications = NULL
  # initializing a counter for the citations
  cstart = 0
  # initializing a boolean that check if the loop should continue
  notstop = TRUE
  
  while (notstop) {
    new_publications = try(get_publications(my_id, cstart=cstart), silent=TRUE)
    if (class(new_publications)=="try-error") {
      notstop = FALSE
    } else {
      # append publication list
      all_publications = rbind(all_publications, new_publications)
      cstart=cstart+20
    }
  }
  return(all_publications)
}

get_abstract = function(pub_id, my_id) {
  print(pub_id)
  paper_url = paste0("http://scholar.google.com/citations?view_op=view_citation&hl=fr&user=",
                     my_id, "&citation_for_view=", my_id,":", pub_id)
  paper_page = htmlTreeParse(paper_url, useInternalNodes=TRUE, encoding="utf-8")
  paper_abstract = xpathSApply(paper_page, "//div[@id='gsc_descr']", xmlValue)
  return(paper_abstract)
}

get_all_abstracts = function(my_id) {
  all_publications = get_all_publications(my_id)
  all_abstracts = sapply(all_publications$pubid, get_abstract, my_id=my_id)
  return(all_abstracts)
}

library(scholar)
library(XML)
library(tm)

my_id = "6hjjIzMAAAAJ"

all_abstracts = get_all_abstracts(my_id)
# transform the abstracts into "plan text documents"
all_abstracts = lapply(all_abstracts, PlainTextDocument)
# find term frequencies within each abstract
terms_freq = lapply(all_abstracts, termFreq, 
                    control=list(removePunctuation=TRUE, stopwords=TRUE, 
                    removeNumbers=TRUE))
# finally obtain the abstract/term frequency matrix
all_words = unique(unlist(lapply(terms_freq, names)))
matrix_terms_freq = lapply(terms_freq, function(astring) {
  res = rep(0, length(all_words))
  res[match(names(astring), all_words)] = astring
  return(res)
})
matrix_terms_freq = Reduce("rbind", matrix_terms_freq)
colnames(matrix_terms_freq) = all_words
# deduce the term frequencies
words_freq = apply(matrix_terms_freq, 2, sum)
# keep only the most frequent and after a bit of cleaning up (not shown) make the word cloud
important = words_freq[words_freq > 10]
library(wordcloud)
wordcloud(names(important), important, random.color=TRUE, random.order=TRUE,
          color=brewer.pal(12, "Set3"), min.freq=1, max.words=length(important), scale=c(3, 0.3))

