var host = location.host;
var host_url = 'http://'+host+'/api';
var PING_URL = '/hello/';
var All_CATEGORIES_URL = '/get-all-categories/';
var All_SUB_CATEGORIES_URL = '/get-all-sub-categories/';
var ALL_ITEMS_URL = '/get-all-items/';
var ADD_TRANSACTION_URL ='/add-transaction/';
var ADD_CATEGORY_URL = '/add_category/';
var ADD_SUB_CATEGORY_URL = '/add-sub-category/';
var ADD_ITEM_URL = '/add-item/';
var ADD_TRANSACTIONS_FROM_SHEET_URL = '/add-transactions-from-sheet/';
var CATEGORIES_SELECT_ELM_ID = 'categoriesSelectId';
var SUB_CATEGORIES_SELECT_ELM_ID = 'subCategoriesSelectId';
var ITEM_SELECT_ELM_ID = 'itemsSelectId';
var ADD_TRANSAC_FORM = 'addTransacFormId';

var tid = setInterval( async () => {
  if ( document.readyState !== 'complete' ) return;
  clearInterval( tid );       
  await main();
}, 100 );

async function main() {
  ping_backend();

  addPostActionForAddTransacForm();

  var categories = await get_categories();
  show_categories(categories);
}

function ping_backend() {
  return fetch_backend(PING_URL).then((data) => {
    console.log(data);
  });
}

function addPostActionForAddTransacForm() {
  var formElm = document.getElementById(ADD_TRANSAC_FORM);
  formElm.addEventListener('submit', getAddTransacFormListener(formElm));
}

function getAddTransacFormListener(formElm) {
  return async (e) => {
    e.preventDefault(); //to prevent form submission

    var payload =new FormData(formElm);

    var res = await fetch_backend(ADD_TRANSACTION_URL, payload);
    console.log(res);
  }
}

async function get_categories() {
  var data = await fetch_backend(All_CATEGORIES_URL); 
  return data.categories;
}

function show_categories(categories) {
  show_data_in_select_element(categories,CATEGORIES_SELECT_ELM_ID);
}

async function onCategorySelected() {
  onSelect(CATEGORIES_SELECT_ELM_ID, get_sub_categories, show_sub_categories);
}

async function get_sub_categories(category) {
  var data = await fetch_backend('/'+category+All_SUB_CATEGORIES_URL );
  return data.sub_categories;
}

function show_sub_categories(subCategories) {
  show_data_in_select_element(subCategories,SUB_CATEGORIES_SELECT_ELM_ID);
}

async function onSubCategorySelected() {
  onSelect(SUB_CATEGORIES_SELECT_ELM_ID, get_items, show_items);
}

async function get_items(sub_category) {
  var data = await fetch_backend('/'+sub_category+ALL_ITEMS_URL);
  return data.items;
}

function show_items(items) {
  show_data_in_select_element(items,ITEM_SELECT_ELM_ID);
}

// function add_transaction(item) {
//   var transc = {category: currentCategory, sub_category: currentSubCategory, item: item, date: date, value: value};
//   return fetch_backend(ADD_TRANSACTION_URL, {transac: transaction});
// }

// function show_transaction(transaction) {
//   console.log(transaction);
// }

function show_data_in_select_element(data, selectElmId) {
  var selectElm = document.getElementById(selectElmId);

  data.forEach( item => {
    var opt = document.createElement('option');
    opt.value = item;
    opt.innerHTML = item;
    selectElm.appendChild(opt);
  });
}

async function onSelect(selectElmId, digestSelectedVal , operate) {
  var selectElm = document.getElementById(selectElmId);
  var selectedVal = selectElm.value;
  
  if(selectedVal == selectElm.options[0].value) {
    return;
  }

  var items = await digestSelectedVal(selectedVal);
  operate(items);
}

function add_item(item) {
  fetch_backend(ADD_ITEM_URL, item).then(function(data) {
    console.log(data);
  });
}

function add_sub_category(sub_category) {
  fetch_backend(ADD_SUB_CATEGORY_URL, sub_category).then(function(data) {
    console.log(data);
  });
}

function add_category(category) {
  fetch_backend(ADD_CATEGORY_URL, category).then(function(data) {
    console.log(data);
  });
}

function upload_sheet(sheet) {
  fetch_backend(ADD_TRANSACTIONS_FROM_SHEET_URL, sheet).then(function(data) {
    console.log(data);
  });
}

async function fetch_backend(routing, payload) {
  var options = null;

  if(payload) {
    // var formData  = new FormData()
    // for(pair of payload) {
    //   formData.append(pair[0],pair[1]);
    // }

    options = {
      method: "POST",
      body: payload
    }
  }

  try {
    var response = await fetch(host_url+routing, options);
  
    if (response.status !== 200) {
      throw('Looks like there was a problem. Status Code: ' +
      response.status);
    }

    return resData = await response.json();

  } catch (error) {
    throw('Fetch Error :-S', error);
  }
}