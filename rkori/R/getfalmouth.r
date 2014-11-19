#' @title Get Falmouth data from the database
#'
#' @description
#' \code{getfalmouth} Query the DB and return data for the period [start_timestamp, end_timestamp)
#' 
#' @family query functions
#' 
#' @details
#' This is a function to trivialize retrieval of the Falmouth data from the rfalmouth view.
#' In order for this function to work, database_connection must be a valid RPostgreSQL connection object
#' And the database view rfalmouth must be present. Note that the command 'Sys.setenv(TZ='GMT')' should
#' always be run before querying the database.
#' 
#' @param database_connection An RPostgreSQL connection object
#' @param start_timestamp (str) A starting timestamp in the form 'YYYY-MM-DD 00:00:00'
#' @param end_timestamp (str) A starting timestamp in the form 'YYYY-MM-DD 00:00:00'
#' @return A dataframe for the period [start_timestamp, end_timestamp)
#' @examples
#' require(RPostgreSQL)
#' con <- dbConnect(PostgreSQL(), host="localhost", user="wkp_user", password="wkp_user", dbname="wkp_hrdb")
#' f <- getfalmouth(con, "2012-11-01 00:00:00", "2012-12-01 00:00:00")
#' qplot(data=f, x=date_time, y=val, colour=site_name) + 
#'      facet_wrap(site_name~var, scales="free_y", nrow=length(levels(f$site_name)), ncol=length(levels(f$var)))
#' @name getfalmouth




getfalmouth <- function(database_connection, start_timestamp, end_timestamp) {
    require(RPostgreSQL)
    #base SQL query
    sql <- "SELECT * from rfalmouth WHERE date_time >= \'STARTDATE\' AND date_time < \'ENDDATE\';"
    
    #Sub start and end timestamps
    sql <- gsub("STARTDATE", start_timestamp, sql)
    sql <- gsub("ENDDATE", end_timestamp, sql)
    
    #query the database
    falmouth <- dbGetQuery(database_connection, sql)
    falmouth$site_name <- as.factor(falmouth$site_name)
    falmouth$var <- as.factor(falmouth$var)
    falmouth$dataset <- as.factor(falmouth$dataset)
    
    #return the data
    return(falmouth)
    }