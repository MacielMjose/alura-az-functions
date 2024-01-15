module.exports = async function (context, req) {
  context.log("JavaScript HTTP trigger function processed a request.");

  // Forçar leitura da configuração do Cosmos DB
  const cosmosDBConnectionString = process.env["azfuncsdatabase_DOCUMENTDB"];
  context.log(`Cosmos DB Connection String: ${cosmosDBConnectionString}`);

  try {
    if (req.query.prioridade && req.query.tarefa) {
      // Set the output binding data from the query object
      context.bindings.tarefaDocument = req.query;

      // Success
      context.res = {
        status: 200,
      };
    } else {
      context.res = {
        status: 400,
        body: "The query options 'prioridade' and 'tarefa' are required",
      };
    }
  } catch (error) {
    context.log.error(`An error occurred: ${error}`);
    context.res = {
      status: 500,
      body: "Internal Server Error",
    };
  }
};
