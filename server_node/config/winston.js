//import logger from 'koa-logger-winston';
import winston from 'winston';
import winstonDaily from 'winston-daily-rotate-file';

const logDir = 'logs'; 
const { combine, timestamp, printf } = winston.format;

// Define log format
   const logFormat = printf(info => {
     return `${info.timestamp} ${info.level}: ${info.message}`;
   });

const CustomLevels = {
	    levels : {
		            error: 0,
		            warn: 1,
		            info: 2,
		            http: 3,
		            
		        },

	    colors: {
		            error: 'red',
		            warn: 'orange',
		            info: 'yellow',
		            http: 'green',
		        }
}

winston.addColors(CustomLevels.colors);

const logger = winston.createLogger({
	  levels: CustomLevels.levels,
	  format: combine(
		      timestamp({
			            format: 'YYYY-MM-DD HH:mm:ss',
			          }),
		      logFormat,
		    ),
	  transports: [
		      
		      
		      new winstonDaily({
			            level: 'error',
			            datePattern: 'YYYY-MM-DD',
			            dirname: logDir + '/error',  
			            filename: `%DATE%.error.log`,
			            maxFiles: 30,
			            zippedArchive: true,
			          }),

		      new winstonDaily({
			              level: 'warn',
			              datePattern: 'YYYY-MM-DD',
			              dirname: logDir + '/warn',  
			              filename: `%DATE%.warn.log`,
			              maxFiles: 30,
			              zippedArchive: true,
			            }),

		       
		      new winstonDaily({
			              level: 'info',
			              datePattern: 'YYYY-MM-DD',
			              dirname: logDir+'/info',
			              filename: `%DATE%.log`,
			              maxFiles: 30,  
			              zippedArchive: true, 
			            }),
		    ],
});

if (process.env.NODE_ENV !== 'production') {
	  logger.add(new winston.transports.Console({
		      format: winston.format.combine(
			            winston.format.colorize(), 
			            winston.format.simple(), 
			          )
		    }));
}

const stream = {
	  write: message => {
		      logger.info(message)
		    }
};

export { logger, stream };
