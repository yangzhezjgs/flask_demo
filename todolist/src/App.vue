<template>
    <div id="app" class="app">
        <h1 v-text='title'></h1>
        <p class='typeInput'>
        <input type="text" v-model='newText' v-on:keyup.enter='addNewlist' >
	<div :class="['form-group', {'has-error': errors.has('text')}]">
	    <span class="help-block" style="color:red"  v-text="errors.get('text')"></span> 
        </div>
	</p>
        <ul>
            <li v-for='item in items'>
		<p v-bind:class='{finished:item.isFinished}' v-on:click='toggleFinish(item)' style='display:inline'>{{item.text}}</p>
  	    	<a v-on:click="delItem(item)">delete</a>
	   </li>
        </ul>
    </div>
</template>

<script>
var axios = require('axios');

class Errors {
  constructor() {
    this.errors = { }
  }

  has(field) {
    return this.errors.hasOwnProperty(field)
  }

  any() {
    return Object.keys(this.errors).length > 0
  }

  get(field) {
    if (this.errors[field]) {
      return this.errors[field][0]
    }
  }

  record(errors) {
    this.errors = errors
  }

  clear(field) {
    delete this.errors[field]  
}
}


export default {
  name: 'app',
  data () {
    return {
      title:'todo list',
      items:[],
      newText:'',
      errors: new Errors()
    }
  },
   methods:{
       toggleFinish:function(item){
         axios.put('/api/item',{'id':item.id}).then(response => {
		if(response.data.ok){
                    item.isFinished=!item.isFinished;
		}})
                },
       addNewlist:function(){
         axios.post('/api/item',{'text':this.newText,'isFinished':false})
		.then(response => {
		if(response.data.ok){
		 this.items.push({
			    id:response.data.id,
                            text:this.newText,
                            isFinished:false
                        })
                   this.newText='';
		   this.errors.clear('text')
		}
             }).catch(error => this.errors.record(error.response.data.errors))
	},
	delItem:function(item){
         axios({
		url: '/api/item',
		method: 'delete',
		data: {
			'id':item.id,
			}
		}
		)
		.then(response => {
		if(response.data.ok){
		 var index = this.items.indexOf(item);
		if (index > -1) {this.items.splice(index, 1)};	
		}})
	}
},

   mounted(){
	axios.get('/api/item',{
	}).then(response =>this.items = response.data)}
	
	
}
</script>

<style>
        *{
            list-style: none;
            outline: none;
            border: none;
        }
        #app{
            text-align: center;
        }
        .app{
            width: 90%;
            margin: 0 auto;
            padding: 5%;
            margin-top: 10px;
        }
        .app li p.finished{
            text-decoration: line-through;
        }    
        .typeInput input{
            width: 50%;
            font-size: 24px;
            border: 1px solid #000;
            padding-left:5px;
        }
</style>
