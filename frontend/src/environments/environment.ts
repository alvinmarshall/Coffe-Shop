/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-cs-fsnd.us', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'QpBpzVgSsnmGApIWGjpGoyPtWP0Lo5df', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:4200', // the base url of the running ionic application.
  }
};
// dev-cs-fsnd.us.auth0.com //domain
// QpBpzVgSsnmGApIWGjpGoyPtWP0Lo5df//client-id

// https://dev-cs-fsnd.us.auth0.com/authorize?audience=coffeeshop&response_type=token&client_id=QpBpzVgSsnmGApIWGjpGoyPtWP0Lo5df&redirect_uri=http://127.0.0.1:4200/tabs/user-page
