const BASE_URL = "https://bit-buddy.onrender.com/";

/** Generate HTML for cryptocurrency */
function generateCryptocurrencyHTML(cryptocurrency) {
  return `
    <div data-cryptocurrency-id=${cryptocurrency.id}>
      <li>
        ${cryptocurrency.name} / ${cryptocurrency.symbol} / ${cryptocurrency.descriptions}
        <button class="delete-button btn-teal">X</button>
        <button class="update-button btn-teal">Update</button>
      </li>
    </div>
  `;
}

/** Fetch and display initial list of cryptocurrencies */
async function showInitialCryptocurrencies() {
  const response = await axios.get(`${BASE_URL}/cryptocurrencies`);

  for (let cryptocurrencyData of response.data.cryptocurrencies) {
    let newCryptocurrency = $(generateCryptocurrencyHTML(cryptocurrencyData));
    $("#cryptocurrencies-list").append(newCryptocurrency);
  }
}

/** Add new cryptocurrency */
$("#new-cryptocurrency-form").on("submit", async function (evt) {
  evt.preventDefault();

  let name = $("#form-name").val();
  let symbol = $("#form-symbol").val();
  let descriptions = $("#form-descriptions").val();

  const newCryptocurrencyResponse = await axios.post(`${BASE_URL}/cryptocurrencies`, {
    name,
    symbol,
    descriptions
  });

  let newCryptocurrency = $(generateCryptocurrencyHTML(newCryptocurrencyResponse.data.cryptocurrency));
  $("#cryptocurrencies-list").append(newCryptocurrency);
  $("#new-cryptocurrency-form").trigger("reset");
});

/** Handle clicking delete: delete cryptocurrency */
$("#cryptocurrencies-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $cryptocurrency = $(evt.target).closest("div");
  let cryptocurrencyId = $cryptocurrency.attr("data-cryptocurrency-id");

  await axios.delete(`${BASE_URL}/cryptocurrencies/${cryptocurrencyId}`);
  $cryptocurrency.remove();
});

/** Function to generate HTML for updating a cryptocurrency */
/** Function to generate HTML for updating a cryptocurrency */
function generateUpdateForm(cryptocurrency) {
    return `
      <form class="update-form">
        <div class="form-row">
          <label for="update-name">Name: </label>
          <input name="name" id="update-name" value="${cryptocurrency.name}">
        </div>
  
        <div class="form-row">
          <label for="update-symbol">Symbol: </label>
          <input name="symbol" id="update-symbol" value="${cryptocurrency.symbol}">
        </div>
  
        <div class="form-row">
          <label for="update-descriptions">Description: </label>
          <input name="descriptions" id="update-descriptions" value="${cryptocurrency.descriptions}">
        </div>
  
        <!-- Submission button for the update form -->
        <button type="submit" class="submit-button">Submit</button>
      </form>
    `;
  }
  

/** Handle clicking update: show update form */
$("#cryptocurrencies-list").on("click", ".update-button", async function (evt) {
  evt.preventDefault();
  let $cryptocurrency = $(evt.target).closest("div");
  let cryptocurrencyId = $cryptocurrency.attr("data-cryptocurrency-id");

  const response = await axios.get(`${BASE_URL}/cryptocurrencies/${cryptocurrencyId}`);
  let cryptocurrency = response.data.cryptocurrency;

  let updateForm = $(generateUpdateForm(cryptocurrency));
  $cryptocurrency.html(updateForm);
});

/** Handle submitting update form */
$("#cryptocurrencies-list").on("submit", ".update-form", async function (evt) {
  evt.preventDefault();
  let $cryptocurrency = $(evt.target).closest("div");
  let cryptocurrencyId = $cryptocurrency.attr("data-cryptocurrency-id");

  // Capture updated values from the form fields
  let name = $cryptocurrency.find("#update-name").val();
  let symbol = $cryptocurrency.find("#update-symbol").val();
  let descriptions = $cryptocurrency.find("#update-descriptions").val();

  // Send PATCH request to update cryptocurrency
  await axios.patch(`${BASE_URL}/cryptocurrencies/${cryptocurrencyId}`, {
    name,
    symbol,
    descriptions
  });

  // Reload the page after successful update
  location.reload();
});



// Show initial list of cryptocurrencies on page load
showInitialCryptocurrencies();
