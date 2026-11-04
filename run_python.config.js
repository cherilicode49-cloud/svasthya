module.exports = {
    apps : [
    {
      name:'svasthya_api',
       script: 'manage.py',
       args: 'runserver 0.0.0.0:8081',
       interpreter : "python" 
    },
    {
      name: 'svashtya_script',
      script: 'manage.py',
      args: 'runscript script',
      interpreter: 'python'
  }
  ]
}
  