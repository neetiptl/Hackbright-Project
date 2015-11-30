//once the page is loaded, populateToDoList
    console.log(this_list_id);
    // debugger;
    var type = $("#list-items").data("type");
    $(document).ready(clickEvent());
    // document.forms[0].reset();

// handle adding to todo lists in db and on screen
    $("#new-todo-item").on("submit", function (evt) {
        evt.preventDefault();
        var formData = $(this).serializeArray();
        $.post('/new_todo/' + this_list_id, formData, populateToDoList);
    });

    $("#new-shopping-item").on("submit", function (evt) {
        evt.preventDefault();
        var formData = $(this).serializeArray();
        $.post('/new_shopping/' + this_list_id, formData, populateShoppingList);
    });


// function to repopulate toDo list displayed with edits
    function clickEvent (){
        $(".doneButton").on("click", function (evt) {
            //identify which button was clicked which item
            var list_type = $("#" + this.id).data("listtype");
            console.log(list_type);         
            var postParams = { 'idOfClickedButton' : this.id, 'listtype' : list_type};
            //go to server and remove from db
            if (list_type == 'ToDo') {
                $.post('/change_task_status', postParams, populateToDoList);
                //return json of full toDo list
            };
            if (list_type == "Shopping") {
                $.post('/change_task_status', postParams, populateShoppingList);
                //return json of full Shopping List
            };
        });
    };

    function populateToDoList (current_list) {
        // debugger;
        $('#list-items-table').empty();
        var json_list = JSON.parse(current_list);
        console.log(json_list);
        console.log(typeof(json_list));

        var tbody = $("#listItemsTable > tbody").html("");
       //for item in toDo List
        for (i=0; i<json_list.length; i++){
            var to_do_id = json_list[i].to_do_id;
            var list_id = json_list[i].list_id;
            var item = json_list[i].item;
            var status_notdone = json_list[i].status_notdone;
            var due_date_todo = json_list[i].due_date_todo;
            var todo_location_name = json_list[i].todo_location_name;
            var todo_location_address = json_list[i].todo_location_address;

            console.log("STATUS", status_notdone);
            var status = "Completed";
            if (status_notdone){
                status = "<input type='button' class='doneButton' data-listtype='ToDo' id=" + to_do_id + " name='status_done'>Incomplete- click if completed";
            }
            else {
                status = "<div id=" + to_do_id + " name='status_done'>Completed!</div>";
            };

            var rowText = "<tr><td>" + item + "</td><td>" + due_date_todo + "</td><td>" + status + "</td><td>" + todo_location_name + "</td><td>" + todo_location_address + "</td></tr>";
            console.log(rowText);
                $(rowText).appendTo(tbody);
        };
        clickEvent();
    };

    function populateShoppingList (current_list) {
        $('#list-items-table').empty();
        var json_list = JSON.parse(current_list);
        console.log(json_list);
        console.log(typeof(json_list));

        var tbody = $("#listItemsTable > tbody").html("");
       //for item in shopping List
        for (i=0; i<json_list.length; i++){
            var shopping_id = json_list[i].shopping_id;
            var list_id = json_list[i].list_id;
            var item = json_list[i].item;
            var status_notdone = json_list[i].status_notdone;
            var due_date_shopping = json_list[i].due_date_shopping;

            console.log("STATUS", status_notdone);
            var status = "Completed";
            if (status_notdone){
                status = "<input type='button' class='doneButton' data-listtype='Shopping' id=" + shopping_id + " name='status_done'>Incomplete- click if completed";
            }
            else {
                status = "<div id=" + shopping_id + " name='status_done'>Completed!</div>";
            };

            var rowText = "<tr><td>" + item + "</td><td>" + status + "</td></tr>";
            console.log(rowText);
                $(rowText).appendTo(tbody);
        };
        clickEvent();
    };
