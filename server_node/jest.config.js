module.exports = {
    testEnvironment: 'node',
    setupFiles: ['./jest.setup.js'], // <- add this
    
    coverageDirectory: 'output/coverage/',
    coverageReporters: ['text-summary', 'html'],
    
    moduleDirectories: [
        "node_modules",
        "src"
    ],
};
