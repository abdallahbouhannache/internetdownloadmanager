import React from "react";
import { useCopyToClipboard } from "usehooks-ts";
import Button from "react-bootstrap/Button";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";

function CopyWrapper({ text, child }) {
  const [value, copy] = useCopyToClipboard();
  const [showTooltip, setShowTooltip] = React.useState(false);

  const handleCopy = () => {
    copy(text);
    // setShowTooltip(true);
    // setTimeout(() => setShowTooltip(false), 150);
    setTimeout(() => {
      copy('');
    }, 5000);
  };

  const renderTooltip = () => {
    return (
      <Tooltip id="copy-tooltip">
        {value ? "Copied!" : "Copy to clipboard"}
      </Tooltip>
    );
  };

  return (
    <OverlayTrigger
      placement="top"
      // show={showTooltip}
      overlay={renderTooltip()}
      delay={300}
    >
      <div style={{cursor:"pointer"}} onClick={handleCopy}>{child}</div>
    </OverlayTrigger>
  );
}

export default CopyWrapper;
