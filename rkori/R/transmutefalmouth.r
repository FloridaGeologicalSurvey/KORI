#' @title Transmute Falmouth data from a long-format vector of factors to a wide-format data frame of vectors
#'
#' @description
#' \code{transmutefalmouth} Transmute Falmouth from a vector of factors to a data frame of vectors
#' 
#' @family manipulation functions
#' 
#' @details
#' This function transmutes Falmouth data from the long format supplied to by getfalmouth() to a wide format, matrix-like dataframe
#' The resulting wide format dataframe is useful with functions that require a matrix or matrix-like input. (Correlation matrices, etc.)
#' Note that it is recommended that this function be used only with the rfalmouth_hourly or rfalmouth_daily view, as differences of minutes or seconds
#' in the time of observation can result mismatch in the final time series.
#' 
#' @param falmouth_dataframe (data frame) A dataframe of the type supplied by the getfalmouth() function
#' @param pivot_factor (str) the factor to transmute. Must be one of the following: 'aspd', 'avdir', 'cond', 'temp', 'pres'
#' @return A matrix-like data frame
#' @examples
#' require(RPostgreSQL)
#' db <- dbConnect(PostgreSQL(), host="localhost", user="wkp_user", password="wkp_user", dbname="wkp_hrdb")
#' fal.hourly <- getfalmouth(db, '2012-06-01 00:00:00', '2012-12-01 00:00:00', dataset="rfalmouth_hourly")
#' head(fal.hourly)
#' str(fal.hourly)
#' hourly.aspd <- transmutefalmouth(fal.hourly, "aspd")
#' head(hourly.aspd)
#' str(hourly.aspd)
#' plot(hourly.aspd[,seq(2, length(hourly.aspd))], pch=20)
#' 
#' #correlation matrix
#' cor(hourly.aspd[,seq(2, length(hourly.aspd))], use="pairwise.complete.obs")
#' heatmap(cor(hourly.aspd[,seq(2, length(hourly.aspd))], use="pairwise.complete.obs"),  col = cm.colors(256), symm=T, margins=c(12,12))
#' @name transmutefalmouth

transmutefalmouth <- function(falmouth_dataframe, pivot_factor) {
    require(reshape2)
    require(plyr)
    transmuted_dataframe <- dcast(falmouth_dataframe, date_time ~ site_name, value.var="val", subset=.(var==pivot_factor))
    return(transmuted_dataframe)
}