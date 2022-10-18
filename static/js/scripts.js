window.addEventListener('DOMContentLoaded', event => {
    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
// warnning ! 여기 아래 리펙토링 필요!!!
window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki
    const datatablesSimple = document.getElementById('datatablesSimple1');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});

window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki
    const datatablesSimple = document.getElementById('datatablesSimple2');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});

// warnning ! 여기 아래 리펙토링 필요!!!
$(document).ready(function (e) {
    $('#upload1').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles1').files.length;
        
        if(ins == 0) {
            $('#msg1').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles1').files[x]);
        }
        form_data.append('filename', document.getElementById('upload1').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg1').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg1').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg1').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg1').html(response.message); // display error response
            }
        });
    });
});

$(document).ready(function (e) {
    $('#upload2').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles2').files.length;
        
        if(ins == 0) {
            $('#msg2').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles2').files[x]);
        }
        form_data.append('filename', document.getElementById('upload2').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg2').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg2').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg2').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg2').html(response.message); // display error response
            }
        });
    });
});

$(document).ready(function (e) {
    $('#upload3').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles3').files.length;
        
        if(ins == 0) {
            $('#msg3').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles3').files[x]);
        }
        form_data.append('filename', document.getElementById('upload3').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg3').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg3').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg3').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg3').html(response.message); // display error response
            }
        });
    });
});

$(document).ready(function (e) {
    $('#upload4').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles4').files.length;
        
        if(ins == 0) {
            $('#msg4').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles4').files[x]);
        }
        form_data.append('filename', document.getElementById('upload4').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg4').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg4').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg4').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg4').html(response.message); // display error response
            }
        });
    });
});


$(document).ready(function (e) {
    $('#upload5').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles5').files.length;
        
        if(ins == 0) {
            $('#msg5').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles5').files[x]);
        }
        form_data.append('filename', document.getElementById('upload5').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg5').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg5').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg5').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg5').html(response.message); // display error response
            }
        });
    });
});


$(document).ready(function (e) {
    $('#upload6').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles6').files.length;
        
        if(ins == 0) {
            $('#msg6').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles6').files[x]);
        }
        form_data.append('filename', document.getElementById('upload6').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg6').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg6').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg6').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg6').html(response.message); // display error response
            }
        });
    });
});


$(document).ready(function (e) {
    $('#upload7').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles7').files.length;
        
        if(ins == 0) {
            $('#msg7').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles7').files[x]);
        }
        form_data.append('filename', document.getElementById('upload7').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg7').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg7').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg7').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg7').html(response.message); // display error response
            }
        });
    });
});

$(document).ready(function (e) {
    $('#upload8').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles8').files.length;
        
        if(ins == 0) {
            $('#msg8').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles8').files[x]);
        }
        form_data.append('filename', document.getElementById('upload8').textContent)
        $.ajax({
            url: 'python-flask-files-upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg8').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg8').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg8').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg8').html(response.message); // display error response
            }
        });
    });
});