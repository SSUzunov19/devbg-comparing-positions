$(function () {
  // Search form submission for positions
  $('#search-form-positions').submit(function (event) {
    event.preventDefault();
    var searchQuery = $('input[name="search-positions"]').val();

    $.ajax({
      url: '/search_positions',
      type: 'GET',
      data: { search: searchQuery },
      success: function (response) {
        displayPositions(response.positions);
      },
      error: function (error) {
        console.log(error);
      }
    });
  });
});

var positionsToCompare = [];

function displayPositions(positions) {
  var container = $('#results');
  container.empty();

  if (positions.length > 0) {
    positions.forEach(function (position) {
      var box = '<div class="box">' +
        '<h2><a href="' + position.link + '">' + position.title + '</a></h2>' +
        '<p>Company: ' + position.company + '</p>' +
        '<p>Location: ' + position.location + '</p>' +
        '<button onclick="addToComparisonPositions(' + JSON.stringify(position).replace(/"/g, '&quot;') + ')">Add to comparison</button>' +
        '</div>';
      container.append(box);
      position.details = box;
    });
  } else {
    container.append('<p>No results found.</p>');
  }
}


// This function adds a position to the positionsToCompare array if there are less than 2 positions in the array.
function addToComparisonPositions(position) {
    if (positionsToCompare.length < 2) {
        // Set the details property to the actual position details
        var jobDescription = position.job_description;
        var shortDescription = jobDescription.substr(0, 500) + '...';
        var descriptionHTML = '<div class="job-description">' + shortDescription + ' <a href="' + position.link + '">Read More</a></div>';
        var categoriesHTML = '<ul>';
        for (var i = 0; i < position.categories.length; i++) {
            categoriesHTML += '<li>' + position.categories[i] + '</li>';
        }
        categoriesHTML += '</ul>';
        position.details = '<table class="compare-table">' +
            '<tr><th>Title</th><td>' + position.title + '</td></tr>' +
            '<tr><th>Company</th><td>' + position.company + '</td></tr>' +
            '<tr><th>Location</th><td>' + position.location + '</td></tr>' +
            '<tr><th>Date</th><td>' + position.date + '</td></tr>' +
            '<tr><th>Categories</th><td>' + categoriesHTML + '</td></tr>' +
            '<tr><th>Job Description</th><td>' + descriptionHTML + '</td></tr>';

        // Add the salary row only if min_salary is not null
        if (position.min_salary !== null) {
            position.details += '<tr><th>Salary</th><td>' + position.min_salary + ' - ' + position.max_salary + '</td></tr>';
        }

        position.details += '</table>';

        // Add the position object to the positionsToCompare array
        positionsToCompare.push(position);
        var positionElement = '<div class="box" id="compare-position-' + position.id + '">' +
            '<h2><a href="' + position.link + '">' + position.title + '</a></h2>' +
            '<p>' + position.company + '</p>' +
            '<p>' + position.location + '</p>' +
            '<button onclick="removeFromComparisonPositions(' + position.id + ')">Remove</button>' +
            '</div>';
        $('#comparison-container').append(positionElement);

        if (positionsToCompare.length === 2) {
            $('#compare-btn-positions').prop('disabled', false);
        }
    } else {
        alert('You can only compare two positions at a time.');
    }
}

// This function removes a position from the positionsToCompare array and from the comparison container.
function removeFromComparisonPositions(id) {
    positionsToCompare = positionsToCompare.filter(function (position) {
        return position.id !== id;
    });
    $('#compare-position-' + id).remove();
    if (positionsToCompare.length < 2) {
        $('#compare-btn-positions').prop('disabled', true);
    }
}

function compareCompanies(company1, company2) {
    var company1Details = { name: 'Company 1', activity: 'Activity 1', sector: 'Sector 1' };
    var company2Details = { name: 'Company 2', activity: 'Activity 2', sector: 'Sector 2' };

    // If the company names match those provided, replace the details with the actual company details
    if (company1 === company1Details.name) {
        company1Details = { name: company1, activity: 'Activity 1', sector: 'Sector 1' };
    }
    if (company2 === company2Details.name) {
        company2Details = { name: company2, activity: 'Activity 2', sector: 'Sector 2' };
    }

    // Create an object containing the details for the two companies
    var response = { company1Details: company1Details, company2Details: company2Details };
    return response;
}

$('#compare-companies-btn').on('click', function () {
  var company1 = $('#company1-input').val();
  var company2 = $('#company2-input').val();
  var comparisonDetails = compareCompanies(company1, company2);
  console.log('Comparison details:', comparisonDetails);

  // Call addToComparison() with the selected company
  var selectedCompany = comparisonDetails.company1Details.name;
  addToComparison(companies.find(company => company.name === selectedCompany));
});


// This function is called when the "Compare" button is clicked for positions.
$('#compare-btn-positions').on('click', function () {
    if (positionsToCompare.length === 2) {
        $('#position1').html(positionsToCompare[0].details);
        $('#position2').html(positionsToCompare[1].details);
        $('#comparison-modal').css('display', 'block');
    } else {
        alert('Please select two positions to compare.');
    }
});

// Get the modal element
var modal = document.getElementById("comparison-modal");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
