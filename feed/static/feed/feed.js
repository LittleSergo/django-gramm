const maxVisibleComments = 3;
const likeUrl = '/static/feed/liked.png'
const doesntLikeUrl = '/static/feed/doesnt_liked.png'

function toggleComments(postId, tabId) {
  const comments = $('#' + tabId + postId + ' .comments' + postId);
  const postComments = comments.find('.comment');

  if (postComments.length > maxVisibleComments) {
    postComments.slice(0, postComments.length - maxVisibleComments).addClass('hidden');
    const expandButton = $('<a class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover d-md-flex justify-content-md-end expand-comments">Expand Comments</a>');
    const collapseButton = $('<a class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover d-md-flex justify-content-md-end collapse-comments">Collapse Comments</a>');

    comments.find('.expand-comments').remove();
    comments.find('.collapse-comments').remove();

    comments.prepend(expandButton);

    comments.on('click', '.expand-comments', function() {
      comments.find('.comment.hidden').removeClass('hidden');
      comments.find('.expand-comments').remove();
      comments.find('.collapse-comments').remove();
      expandButton.remove();
      comments.prepend(collapseButton);
    });

    comments.on('click', '.collapse-comments', function() {
      postComments.slice(0, postComments.length - maxVisibleComments).addClass('hidden');
      comments.find('.expand-comments').remove();
      comments.find('.collapse-comments').remove();
      collapseButton.remove();
      comments.prepend(expandButton);
    });
  };
}

$(document).ready(function() {
  $('.post').each(function() {
    const postId = $(this).attr('id').replace(/feed|post/, '');
    toggleComments(postId, 'feed');
    toggleComments(postId, 'post');
  });

  $('.send-comment').submit(function (e) {
    e.preventDefault();
    var form = $(this);

    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize(),
      dataType: 'json',
      success: function (response) {
        $('.comments' + response.post_id).text('')
        response.comments.forEach(function(comment) {
          $('.comments' + response.post_id).append('<li class="list-group-item comment"><span class="comment-text"><b>' + 
                                                   comment.owner + '</b> '  + comment.text + '</span><span class="comment-posted">' + 
                                                   comment.posted + '</span><span class="comment-like"><span class="comment-likes-count comment-likes-count' + 
                                                   comment.id + '">' + comment.likes_count + ' </span><a onclick="likeComment(' + comment.id + 
                                                   ')"><img class="comment-like-btn comment-like-btn' + comment.id + '"src="' + 
                                                   (comment.liked ? likeUrl : doesntLikeUrl)  + '"width="18px"></a></span></li>')
        });
        $('.input-comment' + response.post_id).val('');
        toggleComments(response.post_id, 'feed');
        toggleComments(response.post_id, 'post');
      }
    });
  });
});


function like(postId) {
  $.ajax({
    type: 'GET',
    url: window.location.origin + '/posts/' + postId + '/like',
    success: function(response){
      $('.likes_count' + postId).text(response.likes_count);
      $('.liked-post' + postId).attr('src', doesntLikeUrl);
      if (response.liked) {
        $('.liked-post' + postId).attr('src', likeUrl);
      };
    }
  })
};

function likeComment(commentId)  {
  $.ajax({
    type: 'GET',
    url: window.location.origin + '/comments/' + commentId + '/like',
    success: function(response) {
      $('.comment-likes-count' + commentId).text(response.likes_count + ' ');
      $('.comment-like-btn' + commentId).attr('src', doesntLikeUrl);
      if (response.liked) {
        $('.comment-like-btn' + commentId).attr('src', likeUrl);
      };
    }
  })
}
