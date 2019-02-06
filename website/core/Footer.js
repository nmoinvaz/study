/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

class Footer extends React.Component {
  docUrl(doc, language) {
    const baseUrl = this.props.config.baseUrl;
    const docsUrl = this.props.config.docsUrl;
    const docsPart = `${docsUrl ? `${docsUrl}/` : ''}`;
    const langPart = `${language ? `${language}/` : ''}`;
    return `${baseUrl}${docsPart}${langPart}${doc}`;
  }

  pageUrl(doc, language) {
    const baseUrl = this.props.config.baseUrl;
    return baseUrl + (language ? `${language}/` : '') + doc;
  }

  render() {
    return (
      <footer className="nav-footer" id="footer">
        <section className="sitemap">
          <a href={this.props.config.baseUrl} className="nav-home">
            {this.props.config.footerIcon && (
              <img
                src={this.props.config.baseUrl + this.props.config.footerIcon}
                alt={this.props.config.title}
                width="66"
                height="58"
              />
            )}
          </a>
          <div>
            <h5>Software</h5>
            <a href="https://www.extractnow.com/">
              ExtractNow
            </a>
            <a href="https://www.websitescreenshots.com/">
              WebShot
            </a>
          </div>
          <div>
            <h5>Programming</h5>
            <a href="https://github.com/nmoinvaz">
              GitHub
            </a>
            <a
              href="https://github.com/nmoinvaz/minizip">
              Minizip
            </a>
            <a href="https://stackoverflow.com/users/610692/nathan-moinvaziri">
              StackOverflow
            </a>
          </div>
          <div>
            <h5>Books</h5>
            <a href="https://www.goodreads.com/review/list/87543537-nathan-moinvaziri">Goodreads</a>
          </div>
        </section>
      </footer>
    );
  }
}

module.exports = Footer;
