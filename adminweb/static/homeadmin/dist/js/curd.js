function checkAll() {
    var all = document.getElementById("checkAll");

    if (all.checked === true) {
        var ones = document.getElementsByName("item");
        for (var i = 0; i <= ones.length; i++) {
            ones[i].checked = true;
        }
    } else {
        var ones = document.getElementsByName("item");
        for (var i = 0; i <= ones.length; i++) {
            ones[i].checked = false;
        }
    }
}

function checkOne() {
    var one=document.getElementsByName("item");
    one.checked=true;
}

function getValues() {
    var valArr=[];
    var ones=document.getElementsByName('item');
    for (var i=0;i<ones.length;i++){
        if (ones[i].checked===true){
            valArr[i]=ones[i].value
        }
    }
    if (valArr.length!==0){
        var vals = valArr.join(',');
        // alert(valArr);
        $.ajax({　　　　　　　
            url:"/batch_del_cookie",　　　　　　　
            type:'POST',
            contenType:'application/json',　　　　　　　
            traditional:true,　　　　　　
            async: false,
            data:{
                'vals':valArr,
                'csrfmiddlewaretoken': $('#csrf_token').val()
            },
            success:function(){
                var info_ = '批量删除成功'
                var ensure = "/select_site/1_10"
                Modal.confirm({
                    msg: info_,
                    title: '操作提示',
                    btnok: '确认',
                    btncl: '取消',
                 }).on(function (e) {
                    if (e) {
                window.location.href=ensure;
            }
        });
            },
            error:function(){
            }
        })
    }
    else {
        Modal.confirm({
            msg: '您没有选中任何数据!',
            title: '操作提示',
            btnok: '确认',
            btncl: '取消',
         })
    }
}

function delsure() {
        Modal.confirm({
            msg: '确定批量删除吗?',
            title: '操作提醒',
            btnok: '确定',
            btncl: '取消',
        }).on(function (e) {
            if (e) {
                getValues();
            }
        });
    }