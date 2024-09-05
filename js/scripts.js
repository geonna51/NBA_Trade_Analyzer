var dataList = [];
var leftsidelist = [];
var rightsidelist = [];

function generateListItem(value) {
    return `<li class="result-item" data-id="${value.player_id}" data-name="${value.player_name}" data-worth="${value.player_worth}">
        ${value.player_name}
        <img src="/static/nba_headshots/${value.player_id}.png" alt="${value.player_name}" style="width: 50px; height: 50px;">
    </li>`;
}

function attachClickListeners() {
    $(".result-item").on("click", function(event) {
        var playerName = $(this).data("name");
        var playerID = $(this).data("id");
        var playerWorth = $(this).data("worth");
        var resultId = $(this).closest('.result').attr('id');
        var searchbox = $(this).closest('.result').prev('.search-box');
        var searchboxID = searchbox.attr('id');
        const leftSidePlayers = JSON.parse(sessionStorage.getItem("leftSideList"))
        const rightSidePlayers = JSON.parse(sessionStorage.getItem("rightSideList"))
        console.log(typeof(searchboxID));
        console.log("Clicked result ID:", resultId);
        console.log("Searchbox clicked:", searchboxID);
        console.log("Name -", playerName, "ID -", playerID, "Worth -", playerWorth);
        storeSide(playerID, searchboxID, playerName, playerWorth);
        // Place the selected player's name in the corresponding search box
        searchbox.val(playerName);
        
        // Store player ID and worth as data attributes
        searchbox.data("player-id", playerID);
        searchbox.data("player-worth", playerWorth);

        // Hide the result list
        $(this).closest('.result').hide();

        event.stopPropagation();
    });
}

function storeSide(playerID, searchboxID, playerName, playerWorth) {
    console.log("Storeside function open");
    if (searchboxID.includes("left")) {
        leftsidelist.push({playerID, searchboxID, playerName, playerWorth});
        console.log("Left player added: ", playerName);
    } else {
        rightsidelist.push({searchboxID, playerID, playerName, playerWorth});
        console.log("Right player added: ", playerName);
    }

    localStorage.setItem("leftSideList", JSON.stringify(leftsidelist));
    localStorage.setItem("rightSideList", JSON.stringify(rightsidelist));
}

function setupCollapseList() {
    $(document).on("click", function(event) {
        var resultbox = $(".result");
        var searchbox = $(".search-box");

        if (!resultbox.is(event.target) && 
            resultbox.has(event.target).length === 0 &&
            !searchbox.is(event.target)) {
            resultbox.hide();
        }
    });
}
function modifyButton(){
    $(document).on("click",".modify",function(){
        console.log("modify button clicked!")
        window.location.href = "/modify-trade";
    })
}
function reenterPlayers(){
    // Clear the existing values in the search boxes
    $('.left-side .search-box, .right-side .search-box').val('').data('player-id', '').data('player-worth', '');
        // Populate the left side search boxes
        leftsidelist.forEach(function(player, index) {
            var searchbox = $('#' + player.searchboxID);
            searchbox.val(player.playerName);
            console.log(searchbox)
            searchbox.data("player-id", player.playerID);
            searchbox.data("player-worth", player.playerWorth);
        });
    
        // Populate the right side search boxes
        rightsidelist.forEach(function(player, index) {
            var searchbox = $('#' + player.searchboxID);
            searchbox.val(player.playerName);
            searchbox.data("player-id", player.playerID);
            searchbox.data("player-worth", player.playerWorth);
        });
}

$(document).ready(function() {
    setupCollapseList();
    modifyButton();
    // Retrieve stored lists
    leftsidelist = JSON.parse(localStorage.getItem("leftSideList")) || [];
    console.log("leftside list:", leftsidelist);
    rightsidelist = JSON.parse(localStorage.getItem("rightSideList")) || [];
    console.log("rightside list:",rightsidelist);
    if(window.location.pathname == "/modify-trade"){
        reenterPlayers();
    }
    $(".search-box").on("input", function() {
        var searchbox = $(this).val();
        var resultDiv = $(this).next(".result");

        $.ajax({
            method: "POST",
            dataType: "json",
            contentType: "application/json",
            url: "/",
            data: JSON.stringify({ text: searchbox }),
            success: function(res) {
                if (searchbox.length >= 1) {
                    dataList = res;
                    var data = "<ul>";
                    $.each(res, function(index, value) {
                        data += generateListItem(value);
                    });
                    data += "</ul>";
                    resultDiv.html(data).slideDown();
                    attachClickListeners();
                } else if (searchbox.trim() === "") {
                    resultDiv.slideUp();
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    });

    $(document).on("click", ".analyze-button", function() {
        console.log("Analyze button clicked");
        var leftPlayers = $(".left-side .search-box").map(function() {
            return $(this).data("player-id");
        }).get();
        var rightPlayers = $(".right-side .search-box").map(function() {
            return $(this).data("player-id");
        }).get();
    
        console.log("Left players:", leftPlayers);
        console.log("Right players:", rightPlayers);
    
        if (leftPlayers.length === 0 || rightPlayers.length === 0) {
            const errorMessage = $("#error-message");
            errorMessage.show();
        } else {
            $.ajax({
                method: "POST",
                url: "/analysis",
                contentType: "application/json",
                data: JSON.stringify({ left: leftPlayers, right: rightPlayers }),
                success: function(response) {
                    if (response.redirect) {
                        console.log("Redirect")
                        window.location.href = response.redirect;
                    }
                },
                error: function(xhr, status, error) {
                    console.log("AJAX error:", status, error);
                }
            });
        }
    });

    $(document).on("click", ".okay-button", function(){
        console.log("okay-button clicked")
        $(this).closest("#error-message").hide();
    });
});
