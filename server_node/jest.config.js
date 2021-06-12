module.exports = {
    testEnvironment: 'node',
    setupFiles: ['./jest.setup.js'], // <- add this

    moduleDirectories: [
        "node_modules",
        "src"
    ]
};
