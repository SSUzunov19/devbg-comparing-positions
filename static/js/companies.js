$(function () {
  // Search form submission
  $('#search-form').submit(function (event) {
    event.preventDefault();
    var searchQuery = $('input[name="search"]').val();

    // Send an AJAX request to the server to retrieve search results
    $.ajax({
      url: '/search_companies',
      type: 'GET',
      data: { search: searchQuery },
      success: function (response) {
        // Display the retrieved search results
        displayCompanies(response.companies);
      },
      error: function (error) {
        console.log(error);
      }
    });
  });
});

var companiesToCompare = [];

// Function to display a list of companies
function displayCompanies(companies) {
  var container = $('#results');
  container.empty();

  if (companies.length > 0) {
    companies.forEach(function (company) {
      // Create HTML elements to display the company details and add a button to add the company to comparison
      var activity = company.activity || '-';
      var sector = company.sector || '-';
      var activityText = '<p>Activity: ' + activity + '</p>';
      var sectorText = '<p>Sector: ' + sector + '</p>';
      var box = '<div class="box">' +
        '<h2><a href="' + company.link + '">' + company.name + '</a></h2>' +
        (company.activity === null ? sectorText : activityText) +
        '<button onclick="addToComparison(' + JSON.stringify(company).replace(/"/g, '&quot;') + ')">Add to comparison</button>' +
        '</div>';
      container.append(box);
      company.details = box;
    });
  } else {
    container.append('<p>No results found.</p>');
  }
}

// Function to add a company to the list of companies to compare
function addToComparison(company) {

  var techList = company.technologies;
  var hiddenTechs = techList.slice(8);
  var showMoreButton = '';

  // If the technologies list has more than 8 items, truncate the list and show a "Show more" button
  if (techList.length > 8) {
    techList = techList.slice(0, 8);
    showMoreButton = '<button class="tech-toggle" onclick="toggleTechList(this)">Show more</button>';
  }

  // If there are less than 2 companies in the list of companies to compare, add the current company to the list
  if (companiesToCompare.length < 2) {
    // Set the details property to the actual company details
    company.details = '<table class="compare-table">' +
      '<tr><th>Name</th><td>' + company.name + '</td></tr>' +
      '<tr><th>Activity</th><td>' + company.activity + '</td></tr>' +
      '<tr><th>Sector</th><td>' + company.sector + '</td></tr>' +
      '<tr><th>Central Office</th><td>' + company.central_office + '</td></tr>' +
      '<tr><th>Technologies</th><td><ul class="tech-list">' + techList.map(t => '<li>' + t + '</li>').join('') + '</ul>' + showMoreButton + '<ul class="tech-list hidden">' + hiddenTechs.map(t => '<li>' + t + '</li>').join('') + '</ul></td></tr>' +
      '<tr><th>Year of Establishment</th><td>' + company.year_of_establishment + '</td></tr>' +
      '<tr><th>Year of Establishment</th><td>' + company.year_of_establishment + '</td></tr>' +
      '<tr><th>Global Employees</th><td>' + company.global_employees + '</td></tr>' +
      '<tr><th>Established in Bulgaria</th><td>' + company.established_in_bulgaria + '</td></tr>' +
      '<tr><th>Employees in Bulgaria</th><td>' + company.employees_in_bulgaria + '</td></tr>' +
      '<tr><th>Offices in Bulgaria</th><td>' + company.offices_in_bulgaria + '</td></tr>' +
      '<tr><th>IT Employees in Bulgaria</th><td>' + company.iT_employees_in_bulgaria + '</td></tr>' +
      '</table>';

    // Add the company object to the companiesToCompare array
    companiesToCompare.push(company);
    // Create a new company element with the company's information and an ID for comparison
    var companyElement = '<div class="box" id="compare-' + company.id + '">' +
      '<h2><a href="' + company.link + '">' + company.name + '</a></h2>' +
      '<button onclick="removeFromComparison(' + company.id + ')">Remove</button>' +
      '</div>';
    // Append the new company element to the comparison container
    $('#comparison-container').append(companyElement);

    // If there are now two companies to compare, enable the Compare button
    if (companiesToCompare.length === 2) {
      $('#compare-btn').prop('disabled', false);
    }

  } else {
    // Otherwise, alert the user that only two companies can be compared at a time
    alert('You can only compare two companies at a time.');
  }
}

// Toggle the display of the technology list when the user clicks the "Show more" button
function toggleTechList(button) {
  var techList = $(button).siblings('.tech-list');
  techList.toggleClass('hidden');

  // Change the text of the button depending on whether the full list is being shown or hidden
  if ($(button).text() === 'Show more') {
    $(button).text('Show less');
  } else {
    $(button).text('Show more');
  }
}

// Remove a company from the comparison array and the comparison container when the "Remove" button is clicked
function removeFromComparison(id) {
  companiesToCompare = companiesToCompare.filter(function (company) {
    return company.id !== id;
  });
  $('#compare-' + id).remove();

  // Disable the Compare button if there are now fewer than two companies to compare
  if (companiesToCompare.length < 2) {
    $('#compare-btn').prop('disabled', true);
  }
}

// When the Compare button is clicked, display the comparison modal if there are two companies to compare
$('#compare-btn').on('click', function () {
  if (companiesToCompare.length === 2) {
    $('#company1').html(companiesToCompare[0].details);
    $('#company2').html(companiesToCompare[1].details);
    $('#comparison-modal').css('display', 'block');
  } else {
    // Otherwise, alert the user to select two companies to compare
    alert('Please select two companies to compare.');
  }
});

// Get the comparison modal and the close button
var modal = document.getElementById("comparison-modal");
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the close button, hide the comparison modal
span.onclick = function () {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, hide it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}