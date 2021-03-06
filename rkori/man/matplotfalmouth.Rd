% Generated by roxygen2 (4.1.0): do not edit by hand
% Please edit documentation in R/matplotfalmouth.r
\name{matplotfalmouth}
\alias{matplotfalmouth}
\title{Plot Falmouth Data}
\usage{
matplotfalmouth(falmouth, scale_type = "free_y", point_size = 1)
}
\arguments{
\item{falmouth}{(dataframe) A dataframe generated by the getfalmouth() function}

\item{scale_type}{(str) A string value giving the scales value for the facet_wrap() function. Valid values are "fixed", "free", "free_x", "free_y". Default value is "free_y".}

\item{point_size}{(numeric) A numeric value giving the point size for plots. Defaults to 1, bt may need adjusting depending on the size of the date range plotted.}
}
\value{
This function returns nothing
}
\description{
\code{matplotfalmouth} Matrix plot of falmouth data returned by the getfalmouth function
}
\details{
This is a function to trivialize plotting the Falmouth data from the rfalmouth view.
The inputs are a falmouth table generated by the getfalmouth() function in the rkori package
And the database view rfalmouth must be present. Note that the command 'Sys.setenv(TZ='GMT')' should
always be run before querying the database.
}
\examples{
require(RPostgreSQL)
require(ggplot2)
Sys.setenv(TZ='GMT')
con <- dbConnect(PostgreSQL(), host="localhost", user="wkp_user", password="wkp_user", dbname="wkp_hrdb")
f <- getfalmouth(con, "2012-11-01 00:00:00", "2012-12-01 00:00:00")
matplotfalmouth(f)
}
\seealso{
Other res: \code{\link{getfalmouth}};
  \code{\link{transmutefalmouth}}
}

