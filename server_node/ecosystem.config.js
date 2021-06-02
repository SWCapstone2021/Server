module.exports = {
	apps: [
		{
			name: 'findyou',
			script: './src/index.js',
			instances: 0,
			exec_mode: 'cluster'
		}
	       ]
}
