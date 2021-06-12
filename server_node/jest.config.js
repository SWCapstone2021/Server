module.exports = {
    testEnvironment: 'node',
    setupFiles: ['./jest.setup.js'], // <- add this
    
    coverageDirectory: 'output/coverage/',
    coverageReporters: ['text-summary', 'html'],
    
    moduleDirectories: [
        "node_modules",
        "src"
    ],
    
    reporters: [
        'default',
        [
          './node_modules/jest-html-reporter',
          {
            pageTitle: 'Test Report',
            outputPath: 'output/test/test-report.html',
          },
        ],
    ],
};
