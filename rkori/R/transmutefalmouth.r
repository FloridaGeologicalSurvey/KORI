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
#' 
#' @param falmouth_dataframe (data frame) A dataframe of the type supplied by the getfalmouth() function
#' @param pivot_factor (str) the factor to transmute. Must be one of the following: 'aspd', 'avdir', 'cond', 'temp', 'pres'
#' @return A matrix-like data frame
#' @examples
#' require(RPostgreSQL)
#' con <- dbConnect(PostgreSQL(), host="localhost", user="wkp_user", password="wkp_user", dbname="wkp_hrdb")
#' fal <- getfalmouth(con, "2012-06-01 00:00:00", "2012-12-01 00:00:00")
#' head(fal)
#' str(fal)
#' fal2 <- transmutefalmouth(f, "aspd")
#' head(fal2)
#' str(fal2)
#' plot(dfal[,seq(2, length(dfal))], pch=20)

#' @name transmutefalmouth

transmutefalmouth <- function(falmouth_dataframe, pivot_factor) {
    require(reshape2)
    require(plyr)
    transmuted_dataframe <- dcast(falmouth_dataframe, date_time ~ site_name, value.var="val", subset=.(var==pivot_factor))
    return(transmuted_dataframe)
}